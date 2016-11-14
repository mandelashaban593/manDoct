def check_illness(post_values):
    from rango.models import Illness
    '''check if a number exists in a phonebook'''
    try:
        check_illness = Illness.objects.get(
            email=post_values['email'],
            pname=post_values['pname'],
            # firstname=post_values['firstname'],
            # lastname=post_values['lastname'],
            gender=post_values['gender'],
            illness=post_values['illness'],
            kin=post_values['kin'],
            kintelno=post_values['kintelno'],
            username=post_values['username'],
            page=post_values['page'],
        )
        return check_illness
    except Exception, e:
        return False


def check_diognosis(post_values):
    from rango.models import Diognosis
    '''check if a number exists in a phonebook'''
    try:
        check_illness = Illness.objects.get(
            dname=post_values['dname'],
            telno=post_values['telno'],
            # firstname=post_values['firstname'],
            # lastname=post_values['lastname'],
            gender=post_values['gender'],
            diognosis=post_values['diognosis'],
            payi=post_values['payi'],
            email=post_values['email'],
        )
        return check_illness
    except Exception, e:
        return False       


        dname = request.POST['dname']
#       telno = request.POST['telno']
#       gender = request.POST['gender']
#       diognosis = request.POST['diognosis']
#       page = request.POST['page']
#       payi = request.POST['payi']
#       email = request.POST['email']