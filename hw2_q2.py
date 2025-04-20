from collections import namedtuple
from enum import Enum

Condition = Enum("Condition", ("CURE", "HEALTHY", "SICK", "DYING", "DEAD"))
Agent = namedtuple("Agent", ("name", "category"))


def meetup(agent_listing: tuple) -> list:
    """Model the outcome of the meetings of pairs of agents.

    The pairs of agents are ((a[0], a[1]), (a[2], a[3]), ...). If there's an uneven
    number of agents, the last agent will remain the same.

    Notes
    -----
    The rules governing the meetings were described in the question. The outgoing
    listing may change its internal ordering relative to the incoming one.

    Parameters
    ----------
    agent_listing : tuple of Agent
        A listing (tuple in this case) in which each element is of the Agent
        type, containing a 'name' field and a 'category' field, with 'category' being
        of the type Condition.

    Returns
    -------
    updated_listing : list
        A list of Agents with their 'category' field changed according to the result
        of the meeting.
    """
    result = [agent for agent in agent_listing if should_exclude_from_meeting(agent)]
    to_meet = [agent for agent in agent_listing if not should_exclude_from_meeting(agent)]
    
    for i in range(0, len(to_meet), 2):
        a1 = to_meet[i]
        if i + 1 == len(to_meet):
            result.append(a1)
        else:
            a2 = to_meet[i + 1]
            after_a1, after_a2 = meet(a1, a2)
            result.append(after_a1)
            result.append(after_a2)
    
    return result

def should_exclude_from_meeting(a1):
    return a1.category in [Condition.HEALTHY, Condition.DEAD]

def meet(a1, a2):
    """Returns the result of interaction between two agents."""
    if Condition.CURE in [a1.category, a2.category]:
        return (Agent(a1.name, improve(a1.category)), Agent(a2.name, improve(a2.category)))
    else:
        return (Agent(a1.name, worsen(a1.category)), Agent(a2.name, worsen(a2.category)))


def improve(condition):
    """Improves the condition by one step."""
    if condition == Condition.DYING:
        return Condition.SICK
    elif condition == Condition.SICK:
        return Condition.HEALTHY
    else:
        return condition

def worsen(condition):
    """Worsens the condition by one step."""
    if condition == Condition.SICK:
        return Condition.DYING
    elif condition == Condition.DYING:
        return Condition.DEAD
    else:
        return condition
