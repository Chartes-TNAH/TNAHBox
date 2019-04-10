def lenTitle(title):
    '''
    Fonction qui mesure la longueur d'une chaine de caractère et renvoie 1 si elle est supérieure à 20 caractères
    :param title: chaine de caractère à mesurer (str)
    :return: 1 (si desc > 20) ou 0 (si desc < 20)
    '''
    if len(title) > 20:
        lentitle = 1
    else:
        lentitle = 0

    return lentitle


def lenDesc(desc):
    '''
    Fonction qui mesure la longueur d'une chaine de caractère et renvoie 1 si elle est supérieure à 60 caractères
    :param desc: chaine de caractère à mesurer (str)
    :return: 1 (si desc > 60) ou 0 (si desc < 60)
    '''
    if len(desc) > 60:
        lendesc = 1
    else:
        lendesc = 0

    return lendesc


def extension_ok(nom_fichier=""):
    """ Renvoie True si le fichier possède une extension valide. """
    return '.' in nom_fichier and nom_fichier.rsplit('.', 1)[1] in ('txt', 'pdf', 'csv', 'doc', 'jpg', 'json',
                                                                    'jpeg', 'gif', 'bmp', 'png', 'word', 'xml', 'py',
                                                                    'odt')