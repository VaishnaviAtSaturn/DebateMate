import random

TOPICS = {
    "Technology": [
        "Artificial intelligence will eliminate more jobs than it creates",
        "Social media does more harm than good to society",
        "Cryptocurrency should replace traditional banking systems",
        "Autonomous vehicles should be allowed on public roads",
        "Big tech companies have too much power over democracy",
        "The metaverse will replace physical social interaction",
        "Facial recognition technology should be banned in public spaces",
        "Open-source software is more secure than proprietary software",
        "5G technology poses significant health risks to humans",
        "Governments should regulate algorithmic content recommendation systems",
        "Quantum computing will make all current encryption obsolete",
        "Space colonization should be funded by private companies, not governments",
    ],
    "Education": [
        "University education should be free for all citizens",
        "Standardized testing does more harm than good to students",
        "Homework should be banned in primary schools",
        "Online learning is as effective as in-person education",
        "School uniforms improve academic performance",
        "Students should be taught coding from primary school",
        "Liberal arts degrees are more valuable than STEM degrees",
        "Private schools should not receive government funding",
        "Mental health education should be mandatory in schools",
        "Student loan debt should be entirely cancelled by governments",
        "The traditional grading system should be abolished",
        "Gap years before university benefit students more than harm them",
    ],
    "Society": [
        "Universal basic income would do more good than harm",
        "The death penalty should be abolished worldwide",
        "Drug use should be decriminalized globally",
        "Voting should be mandatory for all eligible citizens",
        "Social media platforms should be legally responsible for user content",
        "Cancel culture is a threat to free speech",
        "The gender pay gap is primarily caused by discrimination",
        "Immigration has a net positive effect on host countries",
        "Affirmative action creates more equality or more division",
        "The nuclear family is the best structure for raising children",
        "Prisons should focus on rehabilitation rather than punishment",
        "Euthanasia should be legal with strict safeguards",
    ],
    "Business": [
        "Remote work is more productive than office work",
        "The four-day work week should become the global standard",
        "Corporations have a moral obligation to address climate change",
        "Monopolies should be broken up by governments",
        "Minimum wage increases hurt small businesses more than they help workers",
        "Gig economy platforms exploit workers rather than empower them",
        "CEOs are paid too much relative to their employees",
        "Globalization has created more inequality than prosperity",
        "Startups should prioritize growth over profitability",
        "ESG investing (Environmental, Social, Governance) produces better long-term returns",
        "Automation will benefit workers in the long run",
        "Corporate tax rates should be significantly increased",
    ],
    "Environment": [
        "Nuclear energy is the best solution to climate change",
        "Meat consumption should be heavily taxed to reduce emissions",
        "Developed nations should pay climate reparations to developing nations",
        "Individual action is more important than corporate policy for climate change",
        "Plastic packaging should be completely banned",
        "Carbon taxes are the most effective tool to fight climate change",
        "Geoengineering the climate is too risky to pursue",
        "Electric vehicles will solve urban pollution problems",
        "Fast fashion should be regulated to reduce waste",
        "Rewilding natural habitats is more effective than planting trees",
        "The aviation industry should face stricter environmental regulations",
        "A global carbon budget should be legally enforced by the United Nations",
    ],
}


def get_random_topic() -> str:
    """Return a single random topic from all categories."""
    all_topics = get_all_topics()
    return random.choice(all_topics)


def get_all_topics() -> list:
    """Return a flat list of all debate topics across all categories."""
    all_topics = []
    for category_topics in TOPICS.values():
        all_topics.extend(category_topics)
    return all_topics


def get_topics_by_category() -> dict:
    """Return the full dictionary of topics organized by category."""
    return TOPICS
