from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.lib.colors import Color

REPO_URL = "https://github.com/Tsigie-beyene/alx-project-nexus-"
PROJECT_NAME = "Project Nexus — E‑Commerce Backend (ProDev BE)"
AUTHOR = "[Your Name]"

# Colors (RGB in 0-1 range)
COLOR_BG = Color(11/255, 16/255, 32/255)        # dark navy
COLOR_TEXT = Color(245/255, 247/255, 250/255)   # near white
COLOR_MUTED = Color(160/255, 174/255, 192/255)  # gray
COLOR_ACCENT = Color(108/255, 92/255, 231/255)  # purple
COLOR_ACCENT_2 = Color(0/255, 209/255, 178/255) # teal

PAGE_WIDTH, PAGE_HEIGHT = landscape(letter)  # default landscape letter
# Scale to 13.33in x 7.5in for a widescreen feel
PAGE_WIDTH = 13.33 * inch
PAGE_HEIGHT = 7.5 * inch
MARGIN = 0.6 * inch


def draw_footer(c: canvas.Canvas, page_num: int):
    c.setFont("Helvetica", 9)
    c.setFillColor(COLOR_MUTED)
    c.drawString(MARGIN, 0.35 * inch, PROJECT_NAME)
    c.drawRightString(PAGE_WIDTH - MARGIN, 0.35 * inch, str(page_num))


def new_slide(c: canvas.Canvas):
    c.setFillColor(COLOR_BG)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)


def title_slide(c: canvas.Canvas, page_num: int):
    new_slide(c)
    # Accent bar
    c.setFillColor(COLOR_ACCENT)
    c.rect(0, PAGE_HEIGHT - 0.25 * inch, PAGE_WIDTH, 0.25 * inch, fill=1, stroke=0)

    # Title
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica-Bold", 32)
    c.drawString(MARGIN, PAGE_HEIGHT - 2.2 * inch, PROJECT_NAME)

    # Subtitle
    c.setFont("Helvetica", 16)
    c.setFillColor(COLOR_MUTED)
    c.drawString(MARGIN, PAGE_HEIGHT - 3.0 * inch, f"Author: {AUTHOR}  |  GitHub: {REPO_URL}")

    # Links
    c.setFont("Helvetica", 12)
    c.setFillColor(COLOR_ACCENT_2)
    c.drawString(MARGIN, PAGE_HEIGHT - 3.6 * inch, "Links: Repo • Live API • Swagger • ERD • Demo Video")

    draw_footer(c, page_num)
    c.showPage()


def bullets_slide(c: canvas.Canvas, page_num: int, title: str, bullets: list[str]):
    new_slide(c)

    # Title
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(MARGIN, PAGE_HEIGHT - 1.1 * inch, title)

    # Bullets
    y = PAGE_HEIGHT - 1.9 * inch
    c.setFont("Helvetica", 14)
    for line in bullets:
        if y < 1.0 * inch:
            # new page if overflow
            draw_footer(c, page_num)
            c.showPage()
            page_num += 1
            new_slide(c)
            c.setFillColor(COLOR_TEXT)
            c.setFont("Helvetica-Bold", 22)
            c.drawString(MARGIN, PAGE_HEIGHT - 1.1 * inch, title + " (cont.)")
            y = PAGE_HEIGHT - 1.9 * inch
            c.setFont("Helvetica", 14)
        c.setFillColor(COLOR_TEXT)
        c.drawString(MARGIN, y, f"• {line}")
        y -= 0.5 * inch

    draw_footer(c, page_num)
    c.showPage()


def two_column_slide(c: canvas.Canvas, page_num: int, title: str, left: list[str], right: list[str]):
    new_slide(c)

    # Title
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(MARGIN, PAGE_HEIGHT - 1.1 * inch, title)

    # Columns
    col1_x = MARGIN
    col2_x = PAGE_WIDTH / 2 + 0.2 * inch
    y1 = PAGE_HEIGHT - 1.9 * inch
    y2 = PAGE_HEIGHT - 1.9 * inch

    c.setFont("Helvetica", 14)
    for line in left:
        c.setFillColor(COLOR_TEXT)
        c.drawString(col1_x, y1, f"• {line}")
        y1 -= 0.5 * inch

    for line in right:
        c.setFillColor(COLOR_TEXT)
        c.drawString(col2_x, y2, f"• {line}")
        y2 -= 0.5 * inch

    draw_footer(c, page_num)
    c.showPage()


def erd_slide(c: canvas.Canvas, page_num: int):
    new_slide(c)

    # Title
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(MARGIN, PAGE_HEIGHT - 1.1 * inch, "ERD — Core Data Model")

    # Entity boxes
    box_w = 3.5 * inch
    box_h = 2.0 * inch
    y = PAGE_HEIGHT - 3.2 * inch
    x_user = MARGIN
    x_cat = MARGIN + box_w + 0.7 * inch
    x_prod = MARGIN + 2 * (box_w + 0.7 * inch)

    def draw_box(x, y, title, fields):
        c.setFillColor(Color(23/255, 29/255, 50/255))
        c.setStrokeColor(COLOR_ACCENT)
        c.roundRect(x, y, box_w, box_h, 10, stroke=1, fill=1)
        # Title
        c.setFillColor(COLOR_ACCENT_2)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x + 0.25 * inch, y + box_h - 0.5 * inch, title)
        # Fields
        c.setFillColor(COLOR_TEXT)
        c.setFont("Helvetica", 10)
        fy = y + box_h - 0.95 * inch
        for f in fields:
            c.drawString(x + 0.25 * inch, fy, f"- {f}")
            fy -= 0.28 * inch

    draw_box(x_user, y, "User", [
        "id (PK)", "email (unique)", "password_hash", "is_staff",
    ])
    draw_box(x_cat, y, "Category", [
        "id (PK)", "name (unique)", "slug (unique)",
    ])
    draw_box(x_prod, y, "Product", [
        "id (PK)", "name", "description", "price", "stock",
        "category_id (FK)", "created_at", "updated_at",
    ])

    # Relationships legend
    c.setFillColor(COLOR_MUTED)
    c.setFont("Helvetica", 12)
    c.drawString(MARGIN, 1.3 * inch, "Relationships: Category 1—N Product | User used for auth/admin")

    draw_footer(c, page_num)
    c.showPage()


def build_pdf(output_path: str):
    c = canvas.Canvas(output_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    page = 1

    title_slide(c, page); page += 1

    bullets_slide(c, page, "Problem & Goal", [
        "Problem: Power product discovery and management at scale",
        "Users: Shoppers, Admins",
        "Goal: Secure, performant, documented backend with clean APIs",
    ]); page += 1

    bullets_slide(c, page, "Solution Overview", [
        "CRUD: products, categories, users (JWT auth)",
        "Discovery: filtering, sorting, pagination",
        "Quality: indexing, query optimization, OpenAPI docs",
    ]); page += 1

    two_column_slide(c, page, "Tech Stack & Tools",
                     ["Backend: Django, DRF", "DB: PostgreSQL", "Auth: JWT (access/refresh)", "Docs: Swagger/OpenAPI"],
                     ["DevEx: pre-commit, Black, Flake8, isort", "CI/CD: GitHub Actions", "Hosting: Railway/Render/Heroku/VPS", "Observability: Admin, Logs, Health"]);
    page += 1

    bullets_slide(c, page, "Architecture (High Level)", [
        "Client → Django/DRF → PostgreSQL",
        "Optional: Redis for caching/rate limiting",
        "Static/admin: Django Admin",
        "CI: test → lint → migrate → deploy",
    ]); page += 1

    erd_slide(c, page); page += 1

    bullets_slide(c, page, "Database Design Decisions", [
        "Normalization: 3NF; product belongs to one category",
        "Constraints: unique (category.name, category.slug), NOT NULL on critical fields",
        "Indexes: product(category_id, price, created_at)",
        "Optional: trigram/GIN for search on product.name",
    ]); page += 1

    bullets_slide(c, page, "API Design (REST)", [
        "Base: /api/v1/",
        "Auth: POST /auth/login → { access, refresh }",
        "Categories: GET/POST /categories/, GET/PATCH/DELETE /categories/{id}/",
        "Products: GET/POST /products/, GET/PATCH/DELETE /products/{id}/",
        "List params: ?category=<id>&ordering=-price&page=1&page_size=12",
    ]); page += 1

    bullets_slide(c, page, "Filtering, Sorting, Pagination", [
        "Filters: ?category=<id>",
        "Sorting: ?ordering=price or ?ordering=-price",
        "Pagination: ?page=2&page_size=20 (defaults and max limits)",
        "Example: /api/v1/products?category=3&ordering=-price&page=1&page_size=12",
    ]); page += 1

    bullets_slide(c, page, "Authentication & Authorization", [
        "JWT: login returns access + refresh",
        "Password hashing: PBKDF2/Argon2",
        "Permissions: staff/admin required for write; read open",
        "Optional: throttling for sensitive endpoints",
    ]); page += 1

    bullets_slide(c, page, "Performance & Optimization", [
        "ORM: select_related('category') for product lists",
        "Avoid N+1 with prefetch_related",
        "Index verification with EXPLAIN ANALYZE",
        "Optional caching: Redis for popular lists",
    ]); page += 1

    bullets_slide(c, page, "Documentation & Developer Experience", [
        "Swagger/Redoc (OpenAPI)",
        "README: setup, run, env, auth flow, endpoints",
        "Postman collection (optional)",
        "Pre-commit: Black, Flake8, isort",
    ]); page += 1

    bullets_slide(c, page, "Testing & Code Quality", [
        "Unit: serializers, utils",
        "Integration: endpoints (auth, products, categories)",
        "Coverage target: 80%+",
        "CI: tests, lint, migrations check",
    ]); page += 1

    bullets_slide(c, page, "Deployment", [
        "Hosting: Platform + Gunicorn",
        "Environment: secrets via env vars",
        "Health: /health (200 OK)",
        "Run migrations on release",
    ]); page += 1

    bullets_slide(c, page, "Live Demo (≤5 minutes)", [
        "Login: get JWT tokens",
        "Create Category; Create Product (with category)",
        "List Products: filter, sort, paginate",
        "Update/Delete Product (permission gate)",
    ]); page += 1

    bullets_slide(c, page, "Rubric Mapping", [
        "Functionality: CRUD + auth + discovery",
        "Code Quality: readable, docs, linters",
        "Design & API: normalized ERD, RESTful endpoints, DRF ORM",
        "Deployment & Best Practices: live, secure, documented",
    ]); page += 1

    bullets_slide(c, page, "Challenges & Learnings", [
        "Pagination + ordering performance",
        "Auth edge cases and JWT rotation",
        "EXPLAIN plans and index choice",
        "OpenAPI workflows",
    ]); page += 1

    bullets_slide(c, page, "Roadmap", [
        "Features: search, inventory, orders/cart, reviews",
        "Performance: Redis cache, selective indexes",
        "Security: 2FA, admin audit logs, rate limits",
        "Platform: staging, blue/green, observability",
    ]); page += 1

    bullets_slide(c, page, "Links & Access", [
        f"Repo: {REPO_URL}",
        "Live API: [URL]",
        "Swagger/Redoc: [URL]",
        "ERD (Google Doc): [URL – anyone with link can view]",
        "Demo video (≤5 min): [URL]",
        "Slide deck: [Google Slides link]",
        "Health: [URL]/health",
    ]); page += 1

    c.save()


if __name__ == "__main__":
    build_pdf("/workspace/alx_project_nexus_ecommerce.pdf")