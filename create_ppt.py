from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def create_presentation():
    prs = Presentation()
    
    # Custom Theme Colors
    GOLD = RGBColor(0xf0, 0xc0, 0x40)
    TEAL = RGBColor(0x00, 0xe5, 0xcc)
    DARK = RGBColor(0x07, 0x08, 0x0f)

    def set_slide_background(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = DARK

    # Slide 1: Title
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # blank layout
    set_slide_background(slide)
    
    txBox = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(8),(Inches(1)))
    tf = txBox.text_frame
    p = tf.add_paragraph()
    p.text = "StreamAI"
    p.font.bold = True
    p.font.size = Pt(80)
    p.font.color.rgb = GOLD
    p.alignment = PP_ALIGN.CENTER

    txBox2 = slide.shapes.add_textbox(Inches(1), Inches(4), Inches(8),(Inches(0.5)))
    tf2 = txBox2.text_frame
    p2 = tf2.add_paragraph()
    p2.text = "Premium 5G Network Quality Predictor"
    p2.font.size = Pt(28)
    p2.font.color.rgb = TEAL
    p2.alignment = PP_ALIGN.CENTER

    # Slide 2: Problem & Objective
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    set_slide_background(slide)
    title = slide.shapes.title
    title.text = "Problem & Objective"
    title.text_frame.paragraphs[0].font.color.rgb = GOLD
    
    content = slide.placeholders[1]
    content.text_frame.text = "PROBLEM: 5G network instability (Jitter/Latency) makes high-definition streaming unreliable and hard to troubleshoot.\n\nOBJECTIVE: Build an AI-driven system to capture telemetry, analyze stability with RandomForest, and provide a 1-5 quality score."
    for p in content.text_frame.paragraphs:
        p.font.color.rgb = RGBColor(255,255,255)
        p.font.size = Pt(22)

    # Slide 3: The AI Solution
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    set_slide_background(slide)
    title = slide.shapes.title
    title.text = "The AI Solution"
    title.text_frame.paragraphs[0].font.color.rgb = TEAL
    
    content = slide.placeholders[1]
    content.text_frame.text = "• Real-time Telemetry: Automated metric capturing.\n• Machine Learning: RandomForest model trained for 5G.\n• Scientific Ranking: Precise 1-5 Quality Grading.\n• Professional Tickets: Automated PDF session reports."
    for p in content.text_frame.paragraphs:
        p.font.color.rgb = RGBColor(255,255,255)
        p.font.size = Pt(24)

    # Slide 4: Simplified Workflow
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    set_slide_background(slide)
    title = slide.shapes.title
    title.text = "Platform Workflow"
    title.text_frame.paragraphs[0].font.color.rgb = GOLD
    
    content = slide.placeholders[1]
    content.text_frame.text = "1. TELEMETRY: Capture of 6 signal & speed metrics.\n2. AI CHECK: Pattern scanning using trained neural web.\n3. QUALITY SCORE: 1-5 rating with Confidence ratio.\n4. DASHBOARD: Glassmorphic UI with PDF Reports."
    for p in content.text_frame.paragraphs:
        p.font.color.rgb = RGBColor(255,255,255)
        p.font.size = Pt(24)

    # Slide 5: Final Conclusion
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    set_slide_background(slide)
    title = slide.shapes.title
    title.text = "Conclusion & Impact"
    title.text_frame.paragraphs[0].font.color.rgb = TEAL
    
    content = slide.placeholders[1]
    content.text_frame.text = "StreamAI bridges the gap between raw network data and user diagnostics. By using AI-backed scoring (1-5) and cinematic interfaces, it empowers users to optimize their 5G connectivity with visual clarity and scientific reports."
    for p in content.text_frame.paragraphs:
        p.font.color.rgb = RGBColor(255,255,255)
        p.font.size = Pt(24)

    prs.save('StreamAI_Presentation.pptx')
    print("Presentation created successfully: StreamAI_Presentation.pptx")

if __name__ == "__main__":
    create_presentation()
