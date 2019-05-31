from utils.keys import db_password


def get_connection_string(driver):
    return "DRIVER={};Server=tcp:webapp-db-sv.database.windows.net,1433;Database=WebAppDb;" \
           "Uid=BoneyHadger@webapp-db-sv;Pwd={};Encrypt=yes;TrustServerCertificate=no;" \
           "Connection Timeout=30;".format(driver, db_password)


def pass_ownership(user_id, group_id):
    from application import cursor, connection
    # Get all users in the group, except the owner
    cursor.execute("""select UserToGroup.UserID
                      from Groups
                      join UserToGroup on Groups.GroupId = UserToGroup.GroupId
                      where Groups.GroupId = {} and UserID != {}
                   """.format(group_id, user_id))
    new_owner = cursor.fetchone()

    cursor.execute("update Groups set ownerId = {} where GroupId = {}".format(new_owner, group_id))
    connection.commit()


def is_user_member_of_group(user_id, group_id):
    from application import cursor
    cursor.execute(""" select Groups.GroupId
                       from (Groups
                       join UserToGroup on Groups.GroupId = UserToGroup.GroupId)
                       join Users on Users.UserId = UserToGroup.UserId
                       where Users.UserId = {} and Groups.GroupId = {}
                   """.format(user_id, group_id))
    return len(cursor.fetchall()) == 1


def group_has_one_member(group_id):
    from application import cursor
    cursor.execute(""" select count (*)
                       from (Users
                       join UserToGroup on Users.UserId = UserToGroup.UserId)
                       join Groups on Groups.GroupId = UserToGroup.GroupId
                       where Groups.GroupId = {}}
                   """.format(group_id))
    return cursor.fetchone()[0] == 1


def delete_group(group_id):
    from application import cursor
    cursor.execute(""" delete from groups where GroupId = {}""".format(group_id))


def is_group_owner(user_id, group_id):
    from application import cursor
    cursor.execute("select OwnerId from Groups where GroupId = {}".format(group_id))
    return cursor.fetchone()[0] == user_id


def remove_user_from_group(user_id, group_id):
    from application import cursor
    cursor.execute("""delete from UserToGroup where UserId = {} and GroupId = {} """.format(user_id, group_id))

