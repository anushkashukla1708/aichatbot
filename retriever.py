from website import get_portfolio_data


def retrieve(question):

    question = question.lower()

    data = get_portfolio_data()

    if "error" in data:
        return [data]

    knowledge = []

    if any(x in question for x in ["about", "yourself", "who are you"]):
        knowledge.append(data.get("about"))

    if any(x in question for x in ["skill", "technology", "tech"]):
        knowledge.append(data.get("skills"))

    if any(x in question for x in ["education", "college", "cgpa"]):
        knowledge.append(data.get("education"))

    if any(x in question for x in ["experience", "intern"]):
        knowledge.append(data.get("experiences"))

    if any(x in question for x in ["contact", "email", "phone"]):
        knowledge.append(data.get("contact"))

    for project in data.get("projects", []):
        if project["title"].lower() in question:
            knowledge.append(project)

    if "project" in question:
        knowledge.append(data.get("projects"))

    return knowledge