import random
import re
from sqlalchemy.orm import Session
from app.database import models
from app.utils.filters import is_software_job
from app.services.job_service import bulk_save_jobs, get_existing_links
from app.core.browser import get_browser

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
]

async def scrape_internshala(keyword: str, db: Session):

    print("Scraper started")

    browser = get_browser()
    print("Browser obtained")

    clean_term = " ".join([
        w for w in keyword.lower().split()
        if w not in ["internship", "job", "intern"]
    ]).strip() or keyword

    context = await browser.new_context(
        user_agent=random.choice(USER_AGENTS)
    )

    await context.route(
        "**/*",
        lambda r: r.abort()
        if r.request.resource_type in ["image", "media", "font", "stylesheet"]
        else r.continue_()
    )

    page = await context.new_page()

    url = f"https://internshala.com/internships/keywords-{clean_term.replace(' ', '-')}"
    print("Opening URL:", url)

    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_selector(".individual_internship", timeout=15000)

    cards = await page.query_selector_all(".individual_internship")
    print("Cards found:", len(cards))

    existing_links = get_existing_links(db)
    print("Existing links fetched")

    new_jobs = []

    for card in cards:
        title_el = await card.query_selector("h3")
        if not title_el:
            continue

        title = (await title_el.inner_text()).strip()

        if not is_software_job(title, clean_term):
            continue

        href = await card.get_attribute("data-href")
        if not href:
            continue

        link = f"https://internshala.com{href}"

        if link in existing_links:
            continue

        full_text = await card.inner_text()

        stipend_match = re.search(
            r"(₹\s?[\d,]+(\s?-\s?[\d,]+)?(?:\s?/\s?\w+)?|Unpaid|Performance Based)",
            full_text,
            re.IGNORECASE
        )
        stipend = stipend_match.group(0).strip() if stipend_match else "Hidden"

        duration_match = re.search(
            r"(\d+\s?(?:Month|Week)s?)",
            full_text,
            re.IGNORECASE
        )
        duration = duration_match.group(0).strip() if duration_match else "Flexible"

        company_el = await card.query_selector(".company_name")
        company = (await company_el.inner_text()).strip() if company_el else "Unknown"

        skills_el = await card.query_selector(".job_skills")
        skills = "N/A"
        if skills_el:
            raw = await skills_el.inner_text()
            skills = ", ".join([
                s.strip()
                for s in raw.replace("\n", ",").split(",")
                if s.strip()
            ])

        new_jobs.append(
            models.Internship(
                title=title[:200],
                company=company[:100],
                link=link,
                source="Internshala",
                keyword=keyword,
                location="Remote",
                duration=duration[:50],
                stipend=stipend[:100],
                skills=skills[:200]
            )
        )

    print("New jobs collected:", len(new_jobs))

    bulk_save_jobs(db, new_jobs)
    print("Bulk insert completed")

    await context.close()

    return len(new_jobs)