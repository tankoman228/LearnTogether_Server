import DB_Objects.Memoizator as m
from DB_Objects.Group import Group
from DB_Objects.Memoizator import Memoizator

groups = Memoizator(Group)

def create_group(cmd):
    args = str(cmd).split()

    if len(args) != 2:
        print("Bad args. To know what's wrong use help")
        return

    try:
        if int(args[1]):
            print("Group name can't be a number")
            return
    except:
        pass

    groups.save(Group(args[1]))

    #m.save()
    print('success!')


def groups_get_all(cmd):
    #for g in m.get(Group, 999):
    for g in groups.search([], 9999):
        print([g.id, g.name, g.description])


def delete_group(cmd):
    args = str(cmd).split()

    if len(args) != 2:
        print("Bad args. To know what's wrong use help")
        return

    try:
        #gr = m.get(Group, 1, int(args[1]))[0]
        gr = groups.get_by_id(int(args[1]))
        if gr is None:
            return

        print("delete: ", gr.name)
        groups.delete(gr)

        #m.delete(gr)
    except:

        gr = groups.find_by_name(args[1])
        if gr is None:
            return

        print("delete: ", gr.name)
        groups.delete(gr)

        #gr = m.get(Group, 1, args[1])[0]
        #print("delete: ", gr.name)
        #m.delete(gr)