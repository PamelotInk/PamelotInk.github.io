from fpdf import FPDF
import os

OUTPUT = os.path.join(os.path.dirname(__file__), "Portfolio_Skills_Roadmap.pdf")

class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, "Portfolio Skills Roadmap - Pamela Austin", align="L")
        self.cell(0, 8, "May 2026", align="R")
        self.ln(2)
        self.set_draw_color(200, 200, 200)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def title_block(self, text, subtitle):
        self.set_fill_color(30, 58, 95)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 18)
        self.cell(0, 14, text, ln=True, fill=True, align="C")
        self.set_font("Helvetica", "", 10)
        self.cell(0, 8, subtitle, ln=True, fill=True, align="C")
        self.set_text_color(0, 0, 0)
        self.ln(6)

    def tier_header(self, tier_label, tier_title, color_rgb):
        r, g, b = color_rgb
        self.set_fill_color(r, g, b)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, f"  {tier_label} -- {tier_title}", ln=True, fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def section_heading(self, text):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(30, 58, 95)
        self.cell(0, 8, text, ln=True)
        self.set_text_color(0, 0, 0)

    def bullet(self, text, indent=8):
        self.set_font("Helvetica", "", 10)
        x = self.get_x() + indent
        self.set_x(x)
        self.cell(6, 6, "-", ln=False)  # bullet
        effective_width = self.w - self.r_margin - x - 6
        self.multi_cell(effective_width, 6, text)
        self.set_x(self.l_margin)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def note_box(self, text):
        self.set_fill_color(240, 245, 255)
        self.set_draw_color(30, 58, 95)
        self.set_font("Helvetica", "I", 10)
        self.set_text_color(50, 50, 80)
        self.multi_cell(0, 6, text, border=1, fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

    def gap_table(self, rows):
        col_w = [70, 110]
        headers = ["Risk Area", "What to Actually Learn"]
        # Header row
        self.set_fill_color(30, 58, 95)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 10)
        for i, h in enumerate(headers):
            self.cell(col_w[i], 8, h, border=1, fill=True)
        self.ln()
        # Data rows alternate shading
        self.set_text_color(0, 0, 0)
        fills = [(248, 248, 248), (255, 255, 255)]
        for idx, (col1, col2) in enumerate(rows):
            self.set_fill_color(*fills[idx % 2])
            self.set_font("Helvetica", "B", 9)
            # Measure height needed for col2
            lines = self._count_lines(col2, col_w[1] - 4)
            row_h = max(7, lines * 5 + 2)
            y_start = self.get_y()
            self.cell(col_w[0], row_h, col1, border=1, fill=True)
            x_after = self.get_x()
            self.set_font("Helvetica", "", 9)
            self.multi_cell(col_w[1], 5, col2, border=1, fill=True)
            self.set_xy(self.l_margin, y_start + row_h)
        self.ln(4)

    def _count_lines(self, text, width):
        self.set_font("Helvetica", "", 9)
        words = text.split()
        lines, line = 1, ""
        for word in words:
            test = line + (" " if line else "") + word
            if self.get_string_width(test) > width:
                lines += 1
                line = word
            else:
                line = test
        return lines

    def numbered_step(self, number, title, detail):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(30, 58, 95)
        self.cell(8, 7, f"{number}.", ln=False)
        self.cell(0, 7, title, ln=True)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(60, 60, 60)
        self.set_x(self.l_margin + 8)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 8, 5, detail)
        self.set_text_color(0, 0, 0)
        self.ln(1)


pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

# -- TITLE ----------------------------------------------------------------------
pdf.title_block(
    "Portfolio Skills Roadmap",
    "What You Need to Know to Walk the Walk of What Is Showcased"
)

pdf.note_box(
    "This roadmap is derived directly from your portfolio case studies. Each tier reflects how "
    "heavily a skill appears across your projects and how likely a technical interviewer or client "
    "is to probe it. Priority = breadth of coverage + interview exposure risk."
)

pdf.ln(3)

# -- INTRO ----------------------------------------------------------------------
pdf.section_heading("Projects Covered")
projects = [
    "Syilum LLC - Product BI & Self-Service Analytics (2025-Present)",
    "Signet Jewelers - M&A Financial Business Intelligence (Jun-Sep 2025)",
    "AT&T - BI & Self-Service Analytics Platform (Mar 2024-Mar 2025)",
    "AT&T - Marketing Campaign Analytics & Reporting (Mar 2024-Mar 2025)",
    "AT&T - Predictive Analytics & Operational Dashboards (Mar 2024-Mar 2025)",
    "Syilum LLC - Product & Marketing BI, 8-Year Tenure (Jan 2016-Mar 2024)",
    "AT&T/YP Advertising - Marketing Analytics & Data Governance (2013-2016)",
    "Exoplanet Habitability Analysis - Personal ML Project (Nov 2025)",
]
for p in projects:
    pdf.bullet(p)

pdf.ln(5)

# -- TIER 1 ---------------------------------------------------------------------
pdf.tier_header("TIER 1", "Non-Negotiable \"Prove It\" Skills", (30, 58, 95))
pdf.body_text(
    "These appear on nearly every project. You will be asked to demo or whiteboard these. "
    "Not knowing them cold is a significant credibility risk."
)

pdf.section_heading("Advanced SQL")
sql_bullets = [
    "CTEs (WITH clauses) -- chaining multiple logical steps cleanly",
    "Window functions: ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, SUM OVER PARTITION",
    "Conditional aggregation: CASE WHEN inside SUM/COUNT",
    "Funnel queries -- tracking users through sequential steps",
    "Cohort retention logic -- first-event anchoring, day N cohort construction",
    "SCD Type 2 upsert/MERGE logic -- effective dates, surrogate key generation",
    "NULLIF, COALESCE, set-based processing (avoiding row-by-row logic)",
]
for b in sql_bullets:
    pdf.bullet(b)
pdf.ln(3)

pdf.section_heading("Power BI & DAX")
pbi_bullets = [
    "DAX CALCULATE with FILTER -- the core pattern behind nearly every measure",
    "Iterator functions: SUMX, AVERAGEX, RANKX",
    "Time intelligence: DATEADD, SAMEPERIODLASTYEAR, DATESINPERIOD",
    "USERELATIONSHIP -- activating inactive model relationships",
    "Row-Level Security (RLS): static and dynamic, how to test it",
    "Data model design: cardinality, bi-directional filter pitfalls, measure tables",
    "DirectQuery vs. Import mode tradeoffs, incremental refresh",
    "Power Query (M language) -- basic transformations, custom columns",
]
for b in pbi_bullets:
    pdf.bullet(b)
pdf.ln(3)

pdf.section_heading("dbt Core")
dbt_bullets = [
    "Staging -> intermediate -> marts architecture -- why each layer exists",
    "Writing model SQL with Jinja: ref(), source(), config() blocks",
    "Schema tests: not_null, unique, relationships, accepted_values",
    "Custom tests and dbt-expectations / dbt-utils packages",
    "dbt run, dbt test, dbt docs generate, dbt source freshness",
    "GitHub Actions CI/CD pipeline for dbt -- YAML workflow file",
    "Auto-generated lineage docs -- reading the DAG",
]
for b in dbt_bullets:
    pdf.bullet(b)

pdf.ln(5)

# -- TIER 2 ---------------------------------------------------------------------
pdf.tier_header("TIER 2", "Core Functional Proficiency", (0, 112, 60))
pdf.body_text(
    "You must be able to have a real technical conversation and perform basic tasks independently. "
    "Not expert-level, but no blank looks."
)

pdf.section_heading("Snowflake")
sf_bullets = [
    "Virtual warehouses -- sizing, auto-suspend, credits model",
    "Schemas, databases, roles, grants (RBAC basics)",
    "Clustering keys, query pruning, materialized views",
    "Connecting to Power BI: DirectQuery vs. import, incremental refresh",
    "Zero-copy cloning, time-travel (conceptual awareness)",
]
for b in sf_bullets:
    pdf.bullet(b)
pdf.ln(3)

pdf.section_heading("Python for Data")
py_bullets = [
    "Pandas: groupby, merge, pivot_table, melt, apply, handling NaN, datetime",
    "scikit-learn: train_test_split, fit/predict, classification_report, roc_auc_score",
    "RandomForestClassifier, GradientBoostingClassifier, MLPClassifier basics",
    "Feature engineering: derived columns, binning, one-hot encoding",
    "NumPy: array operations, synthetic data generation, numerical computation",
    "SciPy: p-value computation, statistical significance testing",
    "Matplotlib / Seaborn / Plotly -- reading and producing charts",
]
for b in py_bullets:
    pdf.bullet(b)
pdf.ln(3)

pdf.section_heading("Dimensional Modeling")
dm_bullets = [
    "Kimball star schema: fact vs. dimension tables, grain definition",
    "Surrogate keys vs. natural keys -- why surrogate keys matter for SCD",
    "Bridge tables -- resolving many-to-many relationships (e.g., multi-channel attribution)",
    "Conformed dimensions -- sharing dimensions across fact tables",
    "Semantic layer design for self-service (what Power BI 'semantic model' IS)",
]
for b in dm_bullets:
    pdf.bullet(b)
pdf.ln(3)

pdf.section_heading("A/B Testing & Statistics")
ab_bullets = [
    "p-value: what it means and, critically, what it does NOT mean",
    "Statistical power and why you define it BEFORE running a test",
    "Minimum Detectable Effect (MDE) -- choosing a realistic effect size",
    "Type I vs. Type II errors (false positive vs. false negative)",
    "Deterministic hashing for stable cohort assignment (SHA256 mod approach)",
    "Experiment velocity, win rate tracking, novelty effect awareness",
]
for b in ab_bullets:
    pdf.bullet(b)

pdf.ln(5)

# -- TIER 3 ---------------------------------------------------------------------
pdf.tier_header("TIER 3", "Conceptual Fluency", (180, 100, 0))
pdf.body_text(
    "You can be honest that you've used these as part of a broader stack. Know the \"what\" and "
    "\"why\" -- you don't need to write it from scratch, but you must not look puzzled when it comes up."
)

tier3_items = [
    ("Fivetran", "Automated SaaS connectors. Understand what a 'connector' is, schema replication to Snowflake, sync scheduling, and why it replaces hand-written ETL for standard SaaS sources."),
    ("AWS Glue", "Serverless, Spark-based ETL. Know it runs PySpark jobs, is used to extract/transform before loading to a warehouse, and how CloudWatch provides monitoring."),
    ("Salesforce / Workfront", "As data sources. Know the key objects (Lead, Opportunity, Account in SFDC; Task/Project in Workfront), Bulk API 2.0 concept for large extracts."),
    ("SAP FICO / Oracle Financials", "Key tables: BSEG and BKPF (SAP AP/AR journal lines), GL_BALANCES and GL_JE_LINES (Oracle). Know WHY ERP extraction is hard: row-level currency, multiple ledgers, complex join logic."),
    ("GitHub Actions CI/CD", "YAML workflow file structure: trigger (on: push), jobs, steps. How it connects to dbt to run tests on PR before merge. Not writing it from scratch -- reading and explaining it."),
    ("GAAP Concepts (if financial work)","ASC 606 (revenue recognition timing), ASC 842 (lease capitalization). Know the business implication, not the accounting treatment in detail."),
    ("Talend / SSIS", "Legacy ETL tools. Know they do extract-transform-load, are GUI-driven, and are being replaced by cloud-native tools like Glue + dbt. You've used them; you don't need to build new pipelines."),
    ("Master Data Management", "Unified entity records (customer, advertiser). Fuzzy name matching + address standardization for deduplication. Golden record concept."),
    ("RFM Segmentation", "Recency, Frequency, Monetary. Scoring logic, why it predicts churn/LTV. Common in marketing analytics."),
]
for name, detail in tier3_items:
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 7, f">>  {name}", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(60, 60, 60)
    pdf.set_x(pdf.l_margin + 6)
    pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin - 6, 5, detail)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(1)

pdf.ln(4)

# -- TIER 4 ---------------------------------------------------------------------
pdf.tier_header("TIER 4", "Biggest Gap Risks", (180, 30, 30))
pdf.body_text(
    "These are areas where a technical interviewer could quickly expose a gap given how "
    "prominently they appear across your projects. Prioritize closing these."
)

gap_rows = [
    ("dbt -- build it hands-on", "Complete the jaffle_shop tutorial locally. Run dbt run, dbt test, dbt docs. Write a staging model and a mart. This is the single highest-ROI action."),
    ("DAX -- CALCULATE depth", "Practice CALCULATE with FILTER, ALL, REMOVEFILTERS. Build time intelligence measures (MTD, YTD, SPLYY). Understand context transition (row vs. filter context)."),
    ("SCD Type 2 SQL", "Write a working MERGE statement that handles effective dating (valid_from, valid_to, is_current). Understand surrogate key generation with dbt_utils.generate_surrogate_key."),
    ("ML model evaluation", "Confusion matrix, precision vs. recall tradeoff, when to use ROC-AUC vs. accuracy. Know that 96.5% accuracy on imbalanced data can be meaningless."),
    ("Snowflake -- hands-on queries", "Create a free Snowflake trial. Load sample data. Write window function queries. Understand EXPLAIN plans and clustering."),
    ("Python ML end-to-end", "Build one complete pipeline: load data, engineer features, fit a classifier, evaluate with classification_report, plot ROC curve. Use scikit-learn only -- no shortcuts."),
]

pdf.gap_table(gap_rows)

pdf.ln(3)

# -- STARTING ORDER ------------------------------------------------------------
pdf.tier_header("PRACTICAL STARTING ORDER", "Highest ROI First", (60, 60, 60))
pdf.body_text("Follow this sequence. Each step builds on the previous one.")

steps = [
    ("SQL Window Functions", "Every data role tests this. Write cohort retention and funnel queries. Use Mode Analytics, DB Fiddle, or a local Postgres instance to practice."),
    ("DAX CALCULATE Pattern", "This tests Power BI depth faster than anything else. Master context transition and time intelligence. Microsoft Learn's DAX module is free."),
    ("dbt Jaffle Shop Tutorial", "Install dbt-core + dbt-duckdb (no cloud account needed). Complete the full tutorial. This makes the staging/intermediate/marts pattern real and tangible."),
    ("scikit-learn End-to-End", "Pick any Kaggle dataset. Load it, clean it, engineer 3+ features, fit a RandomForest, evaluate. Write the code yourself -- no copy-paste."),
    ("Snowflake Free Trial", "Sign up, load the sample TPCH dataset, write window function queries. Run an EXPLAIN plan. Connect it to Power BI with DirectQuery."),
    ("Statistics for A/B Testing", "Khan Academy Statistics + read \"Trustworthy Online Controlled Experiments\" (Kohavi et al.) -- even just the first 3 chapters. Concepts, not formulas."),
]
for i, (title, detail) in enumerate(steps, 1):
    pdf.numbered_step(i, title, detail)

pdf.ln(4)

# -- MASTER SKILLS CHECKLIST --------------------------------------------------
pdf.add_page()
pdf.set_font("Helvetica", "B", 13)
pdf.set_text_color(30, 58, 95)
pdf.cell(0, 10, "Master Skills Checklist", ln=True)
pdf.set_text_color(0, 0, 0)
pdf.ln(2)

pdf.note_box(
    "Use this as a self-assessment. Rate yourself 1-5 for each item. "
    "Anything below a 3 in Tier 1 or Tier 2 is a study priority."
)

categories = {
    "Cloud & Data Infrastructure": [
        "Snowflake -- querying, warehouse management, roles/grants",
        "AWS Glue -- ETL concepts, Spark-based transformation",
        "Databricks -- distributed compute basics (awareness level)",
        "SQL Server / SSIS -- legacy on-premise ETL",
    ],
    "Data Integration & ETL": [
        "Fivetran -- automated SaaS connector setup & monitoring",
        "dbt Core -- model authoring, testing, CI/CD pipeline",
        "AWS AppFlow / Salesforce Bulk API 2.0",
        "Talend -- legacy ETL tool",
    ],
    "BI & Visualization": [
        "Power BI -- DAX, semantic model, RLS, DirectQuery",
        "Tableau -- workbook design, Tableau Server publishing",
        "Looker -- LookML basics (awareness)",
        "Plotly / Matplotlib / Seaborn -- Python charting",
    ],
    "Programming & Query Languages": [
        "Advanced SQL -- CTEs, window functions, SCD merges",
        "Python -- Pandas, NumPy, SciPy",
        "DAX -- CALCULATE, time intelligence, iterators",
        "YAML -- dbt schema files, GitHub Actions workflows",
    ],
    "Machine Learning & Statistics": [
        "scikit-learn -- classification, evaluation metrics",
        "Random Forest, Gradient Boosting, MLP Neural Network",
        "Statistical significance: p-value, power, MDE",
        "Time series / revenue forecasting concepts",
        "MAPE, R-squared, ROC-AUC -- model evaluation",
        "Feature engineering from domain data",
    ],
    "Analytics Techniques": [
        "A/B testing framework design",
        "Cohort retention analysis",
        "Conversion funnel analysis",
        "Multi-touch attribution modeling",
        "RFM segmentation",
        "Customer / advertiser LTV modeling",
        "Churn prediction modeling",
        "Clickstream / event-level analytics",
        "Budget variance & financial analytics",
    ],
    "Data Modeling": [
        "Star schema / dimensional modeling (Kimball)",
        "SCD Type 1 & Type 2",
        "Bridge tables",
        "Conformed dimensions / semantic layer design",
        "Surrogate key strategy",
    ],
    "Data Governance": [
        "Data dictionary / KPI governance",
        "Master data management & deduplication",
        "Data quality scorecards",
        "SOX compliance / audit trails",
    ],
    "DevOps & Collaboration": [
        "Git / GitHub -- branching, PRs, merge conflict resolution",
        "GitHub Actions CI/CD",
        "Docker basics (container awareness)",
        "Jupyter Notebooks",
    ],
    "Business & Domain Knowledge": [
        "GAAP concepts: ASC 606 (revenue), ASC 842 (leases)",
        "M&A due diligence financial analytics",
        "Marketing attribution & campaign analytics",
        "ERP source systems: SAP FICO, Oracle Financials",
        "CRM systems: Salesforce, Workfront",
    ],
}

for cat, items in categories.items():
    pdf.section_heading(cat)
    for item in items:
        # rating boxes
        pdf.set_font("Helvetica", "", 9)
        pdf.set_x(pdf.l_margin + 4)
        pdf.cell(pdf.w - pdf.l_margin - pdf.r_margin - 4 - 30, 6, f"  {item}", ln=False)
        # draw 5 small rating boxes
        x_boxes = pdf.w - pdf.r_margin - 30
        y_box = pdf.get_y() + 1
        for b in range(5):
            pdf.rect(x_boxes + b * 6, y_box, 5, 4)
        pdf.ln(6)
    pdf.ln(2)

pdf.output(OUTPUT)
print(f"PDF saved to: {OUTPUT}")
