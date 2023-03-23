'''
    Class for representing a node in a search tree for the invitation problem
    Written by Bjornar Tessem, 28.08 2020
'''
import copy
from guest import Guest


class InvitationNode:
    '''
        The class represents the node in a search tree for the invitation csp
    '''

    def __init__(self):
        '''
             A constructor that represent the state of the csp problem at a particular node
        '''
        # Normally one would not hard code data in to a program, but sometimes simplicity is
        # the easiest way to do thing
        # Here you should add all the guests that might be relevant for your party
        # according to the pattern on the next lines
        self.anne = Guest("Anne")
        self.kari = Guest("Kari")
        self.randi = Guest("Randi")
        self.liv = Guest("Liv")
        self.gro = Guest("Gro")
        self.ola = Guest("Ola")
        self.jan = Guest("Jan")
        self.henning = Guest("Henning")
        self.knut = Guest("Knut")
        self.ivar = Guest("Ivar")

        # You also need to make a list of all these potential guests
        self.assignment = [self.anne, self.kari, self.randi, self.liv, self.gro, self.ola, self.jan, self.henning, self.knut, self.ivar]
        self.women = [self.anne, self.kari, self.randi, self.liv, self.gro]
        self.men = [self.ola, self.jan, self.henning, self.knut, self.ivar]

    def get_neighbours(self):
        '''
            Finds the consistent children of a node in the search tree
        :return: a list of children
        '''
        result = []

        n = self.copy_and_add_assignment(Guest.INVITED)
        # generate a child where the next undecided guest is tested for invitation
        if n is not None and n.is_consistent():
            # if there is such a guest and i the invitation assignment is consistent then append n
            result.append(n)

        n = self.copy_and_add_assignment(Guest.NOT_INVITED)
        # generate a child where the next undecided guest is tested for not invitation
        if n is not None and n.is_consistent():
            # if there is such a guest and i the invitation assignment is consistent then append n
            result.append(n)

        return result

    def copy_and_add_assignment(self,invite):
        '''
        Copys a node and adds one invitation status to one potential guest
        :param invite: the invitation status to set
        :return: a node with invitation set for one more guest
        '''
        new_node = copy.deepcopy(self)
        # copy the node
        for guest in new_node.assignment:
            # find a guest that is undecided in self's assignment
            if guest.is_undecided():
                # set this particular guests invitation status to 'invite'
                guest.invited = invite
                return new_node
        return None

    def is_consistent(self):
        '''
        The function that checks if assignments are consistent
        :return: True if an assignment is consistent with the constrain                          ts otherwise False
        '''
        val = True
        # Here we add all the constraints
        # This should not normally be hardcoded in more serious CSP programs.
        #
        # The idea is that only relevant constraints should be checked.
        # To be relevant the node needs to have an assignment that is not UNDECIDED for any of the guests in
        # the constraint. We check this by using the not_relevant_constraint('list of guest objects') function.
        # The parameter to that function should be the guests involved in the constraint
        # So every line below here in the function (except the two last ones) should be of the form
        # val = val and (self.not_relevant_constraint('list of guests in constraint') or ('constraint on one or more guests'))

        # Here you need to fill in the constraints according to the given pattern

        #Constraint 1: If Ola is at the party Anne will not show up.
        val = val and (self.not_relevant_constraint([self.anne, self.ola]) or
                    (self.ola.is_not_invited() or self.anne.is_not_invited()))

        #Constraint 2: If Kari shows up, then Jan will show up. It also goes the other way around.
        val = val and (self.not_relevant_constraint([self.kari, self.jan]) or (
            (self.kari.is_not_invited() or self.jan.is_invited())))

        val = val and (self.not_relevant_constraint([self.kari, self.jan]) or
                       ((self.jan.is_not_invited() or self.kari.is_invited())))

        #Constraint 3: If three of Ola, Ivar, Henning and Knut shows up, others will not be happy.

        val = val and (self.not_relevant_constraint([self.ola, self.ivar, self.henning, self.knut]) or
                    ((self.ola.is_not_invited() or self.ivar.is_not_invited()) or (self.henning.is_not_invited() or self.knut.is_not_invited())))

        #Constraint 4: Randi and Liv can show up together, but they are both in love with Ivar, so if Ivar shows up drama might take place

        val = val and (self.not_relevant_constraint([self.randi, self.liv, self.ivar]) or
                    (self.ivar.is_not_invited() or (self.liv.is_not_invited() or self.randi.is_not_invited())))

        #Constraint 5: Gro has no problem with the other candidates, but she might act a bit dominated in discussions, and Henning and Kari does not like that.

        val = val and (self.not_relevant_constraint([self.gro, self.henning, self.kari]) or
                    (self.gro.is_not_invited() or (self.henning.is_not_invited() and self.kari.is_not_invited())))

        #Constraint 6: If Gro shows up with Knut, Then Jan will get angry

        val = val and (self.not_relevant_constraint([self.gro, self.knut, self.jan]) or
                    ((self.gro.is_not_invited() or self.knut.is_not_invited()) or self.jan.is_not_invited()))

        #Constraint 7: Gro, Anne, Knut and Ola can not be together. Either Gro or Anne dont show up or Knut or Ola dont show up.

        val = val and (self.not_relevant_constraint([self.gro, self.anne, self.knut, self.ola]) or
                    ((self.gro.is_not_invited() or self.anne.is_not_invited()) or (self.knut.is_not_invited() or self.ola.is_not_invited())))

        #Constraint 8: If Ivar dont show up, Henning and Liv does.

        val = val and (self.not_relevant_constraint([self.ivar, self.henning])
                       or (self.ivar.is_invited() or self.henning.is_invited()))

        val = val and (self.not_relevant_constraint([self.ivar, self.liv])
                       or (self.ivar.is_invited() or self.liv.is_invited()))

        
        val = val and self.is_ok_guest_count()
        return val

    def is_ok_guest_count(self):
        count_invited = 0
        count_undecided = 0
        women_invited = 0
        women_undecided = 0
        men_invited = 0
        men_undecided = 0
        for guest in self.assignment:
            if guest.is_invited():
                if guest in self.women:
                    women_invited = women_invited + 1
                elif guest in self.men:
                    men_invited = men_invited +1
                count_invited = count_invited+1
            elif guest.is_undecided():
                if guest in self.women:
                    women_undecided = women_undecided + 1
                elif guest in self.men:
                    men_undecided = men_undecided +1
                count_undecided = count_undecided+1
        # wants exact 6 guests, 3 women and 3 men
        return (count_invited <= 6 and count_invited + count_undecided >= 6 and \
            women_invited <= 3 and women_invited + women_undecided >= 3 and \
            men_invited <= 3 and men_invited + men_undecided >= 3)



    def not_relevant_constraint(self,  constraint_guests):
        '''
        Local function that checks that all guests in a constraint are not UNDECIDED
        :param constraint_guests: the guests involved in a constraint
        :return: True if some guests in the list is UNDECIDED
        '''
        val = False
        for g in constraint_guests:
            if g.is_undecided():
                val = True
        return val

    def is_goal(self):
        '''
        Checks if we are at a goal/leaf in the search tree
        :return: True if all guests have been DECIDED
        '''
        for guest in self.assignment:
            if guest.is_undecided():
                return False
        return True

    def __str__(self):
        '''
        :return: A string representation of an Invitation Node
        '''
        str = ''
        for g in self.assignment:
            if g.invited == Guest.INVITED:
                status = "Invited"
            elif g.invited == Guest.NOT_INVITED:
                status = "Not invited"
            elif g.invited == Guest.UNDECIDED:
                status == "Undecided"
            str = str + '{:6} {}\n'.format(g.name,status)
        return str

