from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def save_chat(messages):

    pdf = SimpleDocTemplate("Chat.pdf")

    styles = getSampleStyleSheet()

    story = []

    for m in messages:

        story.append(
            Paragraph(
                f"<b>{m['role']}</b>: {m['content']}",
                styles["BodyText"]
            )
        )

    pdf.build(story)