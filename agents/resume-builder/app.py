"""
AI Resume Builder — Create professional resumes from user input.
Uses OpenAI GPT-4 to generate polished resume content and FPDF2 for PDF export.
Features 3 template styles: Modern, Classic, and Minimal.
Author: Rayees Yousuf (@RayeesYousufGenAi)
"""

import os
import re
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from fpdf import FPDF
from io import BytesIO

load_dotenv()

st.set_page_config(page_title="📄 AI Resume Builder", page_icon="📄", layout="wide")
st.title("📄 AI Resume Builder")
st.caption("Create professional resumes with AI-powered content generation and PDF export")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def generate_resume_content(personal_info, experience, skills, education):
    """Use GPT-4 to generate professional resume content from user inputs."""

    exp_text = "\n".join(
        f"- {exp['title']} at {exp['company']} ({exp['duration']}): {exp['description']}"
        for exp in experience
    )

    edu_text = "\n".join(
        f"- {edu['degree']} from {edu['institution']} ({edu['year']})"
        for edu in education
    )

    prompt = f"""Create a professional resume summary and polished content based on the following information:

PERSONAL INFO:
Name: {personal_info['name']}
Email: {personal_info['email']}
Phone: {personal_info['phone']}

EXPERIENCE:
{exp_text}

SKILLS:
{', '.join(skills)}

EDUCATION:
{edu_text}

Please provide:
1. A compelling professional summary (2-3 sentences)
2. Polished bullet points for each job experience (2-3 achievements per role)
3. A well-organized skills section

Return the response in this exact format:

SUMMARY:
[Professional summary text]

EXPERIENCE:
[Polished experience bullets]

SKILLS:
[Organized skills list]
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional resume writer. Create polished, ATS-friendly resume content. Use action verbs, quantifiable achievements where possible, and professional tone.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating content: {e}")
        return None


def parse_generated_content(content):
    """Parse the generated content into sections."""
    sections = {"summary": "", "experience": "", "skills": ""}

    if not content:
        return sections

    # Extract summary
    summary_match = re.search(r"SUMMARY:(.+?)(?=EXPERIENCE:|SKILLS:|$)", content, re.DOTALL)
    if summary_match:
        sections["summary"] = summary_match.group(1).strip()

    # Extract experience
    exp_match = re.search(r"EXPERIENCE:(.+?)(?=SKILLS:|$)", content, re.DOTALL)
    if exp_match:
        sections["experience"] = exp_match.group(1).strip()

    # Extract skills
    skills_match = re.search(r"SKILLS:(.+?)$", content, re.DOTALL)
    if skills_match:
        sections["skills"] = skills_match.group(1).strip()

    return sections


class ResumePDF(FPDF):
    """Base PDF class with common functionality."""

    def __init__(self, template="modern"):
        super().__init__()
        self.template = template

    def add_section_header(self, title):
        """Add a section header with template-specific styling."""
        if self.template == "modern":
            self.set_font("Helvetica", "B", 12)
            self.set_text_color(44, 62, 80)
            self.cell(0, 10, title.upper(), ln=True)
            self.set_draw_color(52, 152, 219)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(3)
        elif self.template == "classic":
            self.set_font("Times", "B", 12)
            self.set_text_color(0, 0, 0)
            self.cell(0, 10, title.upper(), ln=True)
            self.set_draw_color(100, 100, 100)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(3)
        else:  # minimal
            self.set_font("Helvetica", "B", 11)
            self.set_text_color(50, 50, 50)
            self.cell(0, 8, title.upper(), ln=True)
            self.ln(2)


def create_modern_pdf(personal_info, sections, experience, education):
    """Create a modern-style resume PDF."""
    pdf = ResumePDF("modern")
    pdf.add_page()

    # Header with colored background
    pdf.set_fill_color(44, 62, 80)
    pdf.rect(0, 0, 210, 50, "F")

    # Name
    pdf.set_xy(10, 15)
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, personal_info["name"], ln=True, align="C")

    # Contact info
    pdf.set_xy(10, 32)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(200, 200, 200)
    contact = f"{personal_info['email']} | {personal_info['phone']}"
    pdf.cell(0, 8, contact, ln=True, align="C")

    pdf.ln(15)

    # Summary
    pdf.add_section_header("Professional Summary")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 6, sections.get("summary", ""))
    pdf.ln(5)

    # Experience
    pdf.add_section_header("Experience")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    for exp in experience:
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 6, f"{exp['title']} | {exp['company']}", ln=True)
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 5, exp["duration"], ln=True)
        pdf.set_text_color(60, 60, 60)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 5, exp["description"])
        pdf.ln(3)

    pdf.ln(3)

    # Education
    pdf.add_section_header("Education")
    for edu in education:
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 6, edu["degree"], ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 5, f"{edu['institution']} | {edu['year']}", ln=True)
        pdf.ln(2)

    pdf.ln(3)

    # Skills
    pdf.add_section_header("Skills")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 6, sections.get("skills", ""))

    return pdf.output(dest="S").encode("latin1")


def create_classic_pdf(personal_info, sections, experience, education):
    """Create a classic-style resume PDF."""
    pdf = ResumePDF("classic")
    pdf.add_page()

    # Name
    pdf.set_font("Times", "B", 28)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 12, personal_info["name"], ln=True, align="C")

    # Contact info
    pdf.set_font("Times", "", 11)
    pdf.set_text_color(60, 60, 60)
    contact = f"{personal_info['email']} | {personal_info['phone']}"
    pdf.cell(0, 8, contact, ln=True, align="C")

    pdf.ln(8)

    # Summary
    pdf.add_section_header("Professional Summary")
    pdf.set_font("Times", "", 11)
    pdf.multi_cell(0, 6, sections.get("summary", ""))
    pdf.ln(5)

    # Experience
    pdf.add_section_header("Experience")
    for exp in experience:
        pdf.set_font("Times", "B", 11)
        pdf.cell(0, 7, f"{exp['title']} - {exp['company']}", ln=True)
        pdf.set_font("Times", "I", 10)
        pdf.cell(0, 5, exp["duration"], ln=True)
        pdf.set_font("Times", "", 11)
        pdf.multi_cell(0, 6, exp["description"])
        pdf.ln(4)

    # Education
    pdf.add_section_header("Education")
    for edu in education:
        pdf.set_font("Times", "B", 11)
        pdf.cell(0, 7, edu["degree"], ln=True)
        pdf.set_font("Times", "", 10)
        pdf.cell(0, 5, f"{edu['institution']}, {edu['year']}", ln=True)
        pdf.ln(3)

    # Skills
    pdf.add_section_header("Skills")
    pdf.set_font("Times", "", 11)
    pdf.multi_cell(0, 6, sections.get("skills", ""))

    return pdf.output(dest="S").encode("latin1")


def create_minimal_pdf(personal_info, sections, experience, education):
    """Create a minimal-style resume PDF."""
    pdf = ResumePDF("minimal")
    pdf.add_page()

    # Name
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 10, personal_info["name"], ln=True)

    # Contact info
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, f"{personal_info['email']} | {personal_info['phone']}", ln=True)

    pdf.ln(10)

    # Summary
    pdf.add_section_header("About")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 5, sections.get("summary", ""))
    pdf.ln(5)

    # Experience
    pdf.add_section_header("Experience")
    for exp in experience:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 6, exp["title"], ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 5, f"{exp['company']} | {exp['duration']}", ln=True)
        pdf.set_text_color(60, 60, 60)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 5, exp["description"])
        pdf.ln(4)

    # Education
    pdf.add_section_header("Education")
    for edu in education:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 6, edu["degree"], ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 5, f"{edu['institution']} | {edu['year']}", ln=True)
        pdf.ln(3)

    # Skills
    pdf.add_section_header("Skills")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 5, sections.get("skills", ""))

    return pdf.output(dest="S").encode("latin1")


def generate_pdf(personal_info, sections, experience, education, template):
    """Generate PDF based on selected template."""
    if template == "Modern":
        return create_modern_pdf(personal_info, sections, experience, education)
    elif template == "Classic":
        return create_classic_pdf(personal_info, sections, experience, education)
    else:  # Minimal
        return create_minimal_pdf(personal_info, sections, experience, education)


# Sidebar for inputs
with st.sidebar:
    st.header("Your Information")

    # Personal Info
    st.subheader("Personal Info")
    name = st.text_input("Full Name", placeholder="Jane Doe")
    email = st.text_input("Email", placeholder="jane@example.com")
    phone = st.text_input("Phone", placeholder="+1 (555) 123-4567")

    # Experience
    st.subheader("Experience")
    if "experience" not in st.session_state:
        st.session_state.experience = []

    with st.expander("Add Experience", expanded=len(st.session_state.experience) == 0):
        exp_title = st.text_input("Job Title", key="exp_title", placeholder="Software Engineer")
        exp_company = st.text_input("Company", key="exp_company", placeholder="Tech Corp")
        exp_duration = st.text_input("Duration", key="exp_duration", placeholder="Jan 2020 - Present")
        exp_desc = st.text_area("Description", key="exp_desc", placeholder="Key responsibilities and achievements")

        if st.button("Add Job", key="add_exp"):
            if exp_title and exp_company:
                st.session_state.experience.append({
                    "title": exp_title,
                    "company": exp_company,
                    "duration": exp_duration,
                    "description": exp_desc,
                })
                st.rerun()

    # Display added experience
    for i, exp in enumerate(st.session_state.experience):
        st.caption(f"✓ {exp['title']} at {exp['company']}")

    # Skills
    st.subheader("Skills")
    skills_input = st.text_area(
        "Skills (comma-separated)",
        placeholder="Python, Machine Learning, Data Analysis, Communication",
    )
    skills = [s.strip() for s in skills_input.split(",") if s.strip()]

    # Education
    st.subheader("Education")
    if "education" not in st.session_state:
        st.session_state.education = []

    with st.expander("Add Education", expanded=len(st.session_state.education) == 0):
        edu_degree = st.text_input("Degree", key="edu_degree", placeholder="Bachelor of Science in Computer Science")
        edu_institution = st.text_input("Institution", key="edu_institution", placeholder="University Name")
        edu_year = st.text_input("Year", key="edu_year", placeholder="2015 - 2019")

        if st.button("Add Education", key="add_edu"):
            if edu_degree and edu_institution:
                st.session_state.education.append({
                    "degree": edu_degree,
                    "institution": edu_institution,
                    "year": edu_year,
                })
                st.rerun()

    # Display added education
    for i, edu in enumerate(st.session_state.education):
        st.caption(f"✓ {edu['degree'][:30]}...")

    # Template Selection
    st.subheader("Template")
    template = st.selectbox("Choose Template", ["Modern", "Classic", "Minimal"])

    # Generate Button
    st.markdown("---")
    generate_btn = st.button("✨ Generate Resume", type="primary", use_container_width=True)

# Main content area
if generate_btn and name and email and st.session_state.experience:
    personal_info = {"name": name, "email": email, "phone": phone}

    with st.spinner("Generating your professional resume..."):
        generated_content = generate_resume_content(
            personal_info, st.session_state.experience, skills, st.session_state.education
        )

    if generated_content:
        sections = parse_generated_content(generated_content)

        # Preview
        st.subheader("📝 Resume Preview")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"### {name}")
            st.caption(f"📧 {email} | 📞 {phone}")
            st.markdown("---")

            st.markdown("**Professional Summary**")
            st.write(sections.get("summary", "N/A"))

            st.markdown("**Experience**")
            for exp in st.session_state.experience:
                st.markdown(f"**{exp['title']}** | *{exp['company']}*")
                st.caption(exp["duration"])
                st.write(exp["description"])

            st.markdown("**Education**")
            for edu in st.session_state.education:
                st.markdown(f"**{edu['degree']}** | *{edu['institution']}* ({edu['year']})")

            st.markdown("**Skills**")
            st.write(sections.get("skills", "N/A"))

        with col2:
            st.info(f"Template: **{template}**")

            # Generate PDF
            pdf_bytes = generate_pdf(
                personal_info, sections, st.session_state.experience, st.session_state.education, template
            )

            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name=f"{name.replace(' ', '_')}_Resume.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

            st.success("Resume ready for download!")

else:
    if generate_btn:
        if not name:
            st.warning("Please enter your name")
        if not email:
            st.warning("Please enter your email")
        if not st.session_state.experience:
            st.warning("Please add at least one work experience")

    # Instructions
    st.info(
        """👈 Fill in your information in the sidebar to generate your professional resume.

**Steps:**
1. Enter your personal information
2. Add work experience (can add multiple)
3. Add skills as comma-separated values
4. Add education (can add multiple)
5. Choose a template style
6. Click "Generate Resume" to preview and download

**Template Styles:**
- **Modern**: Contemporary design with sidebar accent
- **Classic**: Traditional layout with serif fonts
- **Minimal**: Clean, uncluttered design
"""
    )
