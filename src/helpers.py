def find_private_role(member):
    for role in member.roles:
        if len(role.members) == 1 and not role.is_premium_subscriber():
            return role
