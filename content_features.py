import requests
import re


#################################################################################################################################
#               Number of hyperlinks present in a website (Kumar Jain'18)
#################################################################################################################################

# def nb_hyperlinks(Href, Link, Media, Form, CSS, Favicon):
#     return len(Href['internals']) + len(Href['externals']) +\
#            len(Link['internals']) + len(Link['externals']) +\
#            len(Media['internals']) + len(Media['externals']) +\
#            len(Form['internals']) + len(Form['externals']) +\
#            len(CSS['internals']) + len(CSS['externals']) +\
#            len(Favicon['internals']) + len(Favicon['externals'])

def nb_hyperlinks(dom):
    return len(dom.find("href")) + len(dom.find("src"))

#################################################################################################################################
#               Internal hyperlinks ratio (Kumar Jain'18)
#################################################################################################################################


def h_total(Href, Link, Media, Form, CSS, Favicon):
    return nb_hyperlinks(Href, Link, Media, Form, CSS, Favicon)

def h_internal(Href, Link, Media, Form, CSS, Favicon):
    return len(Href['internals']) + len(Link['internals']) + len(Media['internals']) +\
           len(Form['internals']) + len(CSS['internals']) + len(Favicon['internals'])


def internal_hyperlinks(Href, Link, Media, Form, CSS, Favicon):
    total = h_total(Href, Link, Media, Form, CSS, Favicon)
    if total == 0:
        return 0
    else :
        return h_internal(Href, Link, Media, Form, CSS, Favicon)/total


#################################################################################################################################
#               External hyperlinks ratio (Kumar Jain'18)
#################################################################################################################################


def h_external(Href, Link, Media, Form, CSS, Favicon):
    return len(Href['externals']) + len(Link['externals']) + len(Media['externals']) +\
           len(Form['externals']) + len(CSS['externals']) + len(Favicon['externals'])
           
           
def external_hyperlinks(Href, Link, Media, Form, CSS, Favicon):
    total = h_total(Href, Link, Media, Form, CSS, Favicon)
    if total == 0:
        return 0
    else :
        return h_external(Href, Link, Media, Form, CSS, Favicon)/total


#################################################################################################################################
#               Number of null hyperlinks (Kumar Jain'18)
#################################################################################################################################

def h_null(hostname, Href, Link, Media, Form, CSS, Favicon):
    return len(Href['null']) + len(Link['null']) + len(Media['null']) + len(Form['null']) + len(CSS['null']) + len(Favicon['null'])

def null_hyperlinks(hostname, Href, Link, Media, Form, CSS, Favicon):
    total = h_total(Href, Link, Media, Form, CSS, Favicon)
    if total==0:
        return 0
    return h_null(hostname, Href, Link, Media, Form, CSS, Favicon)/total

#################################################################################################################################
#               Extrenal CSS (Kumar Jain'18)
#################################################################################################################################


def external_css(CSS):
    return len(CSS['externals'])
    

#################################################################################################################################
#               Internal redirections (Kumar Jain'18)
#################################################################################################################################


def h_i_redirect(Href, Link, Media, Form, CSS, Favicon):
    count = 0
    for link in Href['internals']:
        try:
            r = requests.get(link)
            if len(r.history) > 0:
                count+=1
        except:
            continue
    for link in Link['internals']:
        try:
            r = requests.get(link)
            if len(r.history) > 0:
                count+=1
        except:
            continue
    for link in Media['internals']:
        try:
            r = requests.get(link)
            if len(r.history) > 0:
                count+=1
        except:
            continue
    for link in Form['internals']:
        try:
            r = requests.get(link)
            if len(r.history) > 0:
                count+=1
        except:
            continue
    for link in CSS['internals']:
        try:
            r = requests.get(link)
            if len(r.history) > 0:
                count+=1
        except:
            continue
    for link in Favicon['internals']:
        try:
            r = requests.get(link)
            if len(r.history) > 0:
                count+=1
        except:
            continue
    return count

def internal_redirection(Href, Link, Media, Form, CSS, Favicon):
    internals = h_internal(Href, Link, Media, Form, CSS, Favicon)
    if (internals>0):
        return h_i_redirect(Href, Link, Media, Form, CSS, Favicon)/internals
    return 0

#################################################################################################################################
#               External redirections (Kumar Jain'18)
#################################################################################################################################


def h_e_redirect(Href, Link, Media, Form, CSS, Favicon):
    count = 0
    for link in Href['externals']:
        try:
            r = requests.get(link)
            if len(r.history) > 0:
                count+=1
        except:
            continue
    for link in Link['externals']:
        try:
            r = requests.get(link)
            if len(r.history) > 0:
                count+=1
        except:
            continue
    for link in Media['externals']:
        try:
            r = requests.get(link)
            if len(r.history) > 0:
                count+=1
        except:
            continue
    for link in Media['externals']:
        try:
            r = requests.get(link)
            if len(r.history) > 0:
                count+=1
        except:
            continue 
    for link in Form['externals']:
        try:
            r = requests.get(link)
            if len(r.history) > 0:
                count+=1
        except:
            continue    
    for link in CSS['externals']:
        try:
            r = requests.get(link)
            if len(r.history) > 0:
                count+=1
        except:
            continue    
    for link in Favicon['externals']:
        try:
            r = requests.get(link)
            if len(r.history) > 0:
                count+=1
        except:
            continue    
    return count

def external_redirection(Href, Link, Media, Form, CSS, Favicon):
    externals = h_external(Href, Link, Media, Form, CSS, Favicon)
    if (externals>0):
        return h_e_redirect(Href, Link, Media, Form, CSS, Favicon)/externals
    return 0



#################################################################################################################################
#               Generates internal errors (Kumar Jain'18)
#################################################################################################################################

def h_i_error(Href, Link, Media, Form, CSS, Favicon):
    count = 0
    for link in Href['internals']:
        try:
            if requests.get(link).status_code >=400:
                count+=1
        except:
            continue
    for link in Link['internals']:
        try:
            if requests.get(link).status_code >=400:
                count+=1
        except:
            continue
    for link in Media['internals']:
        try:
            if requests.get(link).status_code >=400:
                count+=1
        except:
            continue
    for link in Form['internals']:
        try:
            if requests.get(link).status_code >=400:
                count+=1
        except:
            continue
    for link in CSS['internals']:
        try:
            if requests.get(link).status_code >=400:
                count+=1
        except:
            continue  
    for link in Favicon['internals']:
        try:
            if requests.get(link).status_code >=400:
                count+=1
        except:
            continue
    return count

def internal_errors(Href, Link, Media, Form, CSS, Favicon):
    internals = h_internal(Href, Link, Media, Form, CSS, Favicon)
    if (internals>0):
        return h_i_error(Href, Link, Media, Form, CSS, Favicon)/internals
    return 0

#################################################################################################################################
#               Generates external errors (Kumar Jain'18)
#################################################################################################################################


def h_e_error(Href, Link, Media, Form, CSS, Favicon):
    count = 0
    for link in Href['externals']:
        try:
            if requests.get(link).status_code >=400:
                count+=1
        except:
            continue
    for link in Link['externals']:
        try:
            if requests.get(link).status_code >=400:
                count+=1
        except:
            continue
    for link in Media['externals']:
        try:
            if requests.get(link).status_code >=400:
                count+=1
        except:
            continue
    for link in Form['externals']:
        try:
            if requests.get(link).status_code >=400:
                count+=1
        except:
            continue
    for link in CSS['externals']:
        try:
            if requests.get(link).status_code >=400:
                count+=1
        except:
            continue
    for link in Favicon['externals']:
        try:
            if requests.get(link).status_code >=400:
                count+=1
        except:
            continue
    return count


def external_errors(Href, Link, Media, Form, CSS, Favicon):
    externals = h_external(Href, Link, Media, Form, CSS, Favicon)
    if (externals>0):
        return h_e_error(Href, Link, Media, Form, CSS, Favicon)/externals
    return 0


#################################################################################################################################
#               Having login form link (Kumar Jain'18)
#################################################################################################################################

def login_form(Form):
    p = re.compile('([a-zA-Z0-9\_])+.php')
    if len(Form['externals'])>0 or len(Form['null'])>0:
        return 1
    for form in Form['internals']+Form['externals']:
        if p.match(form) != None :
            return 1
    return 0

#################################################################################################################################
#               Having external favicon (Kumar Jain'18)
#################################################################################################################################

def external_favicon(Favicon):
    if len(Favicon['externals'])>0:
        return 1
    return 0


#################################################################################################################################
#               Submitting to email 
#################################################################################################################################

def submitting_to_email(Form):
    for form in Form['internals'] + Form['externals']:
        if "mailto:" in form or "mail()" in form:
            return 1
        else:
            return 0
    return 0


#################################################################################################################################
#               Percentile of internal media <= 61 : Request URL in Zaini'2019 
#################################################################################################################################

def internal_media(Media):
    total = len(Media['internals']) + len(Media['externals'])
    internals = len(Media['internals'])
    try:
        percentile = internals / float(total) * 100
    except:
        return 0
    
    return percentile

#################################################################################################################################
#               Percentile of external media : Request URL in Zaini'2019 
#################################################################################################################################

def external_media(Media):
    total = len(Media['internals']) + len(Media['externals'])
    externals = len(Media['externals'])
    try:
        percentile = externals / float(total) * 100
    except:
        return 0
    
    return percentile

#################################################################################################################################
#               Check for empty title 
#################################################################################################################################

def empty_title(Title):
    if Title:
        return 0
    return 1


#################################################################################################################################
#               Percentile of safe anchor : URL_of_Anchor in Zaini'2019 (Kumar Jain'18)
#################################################################################################################################

def safe_anchor(Anchor):
    total = len(Anchor['safe']) +  len(Anchor['unsafe'])
    unsafe = len(Anchor['unsafe'])
    try:
        percentile = unsafe / float(total) * 100
    except:
        return 0
    return percentile 

#################################################################################################################################
#               Percentile of internal links : links_in_tags in Zaini'2019 but without <Meta> tag
#################################################################################################################################

def links_in_tags(Link):
    total = len(Link['internals']) +  len(Link['externals'])
    internals = len(Link['internals'])
    try:
        percentile = internals / float(total) * 100
    except:
        return 0
    return percentile

#################################################################################################################################
#              Server Form Handler  : sfh in Zaini'2019
#################################################################################################################################

def sfh(hostname, Form):
    if len(Form['null'])>0:
        return 1
    return 0

#################################################################################################################################
#              IFrame Redirection
#################################################################################################################################

def iframe(IFrame):
    if len(IFrame['invisible'])> 0: 
        return 1
    return 0

#################################################################################################################################
#              Onmouse action
#################################################################################################################################

def onmouseover(content):
    if 'onmouseover="window.status=' in str(content).lower().replace(" ",""):
        return 1
    else:
        return 0

#################################################################################################################################
#              Pop up window
#################################################################################################################################

def popup_window(content):
    if "prompt(" in str(content).lower():
        return 1
    else:
        return 0

#################################################################################################################################
#              Right_clic action
#################################################################################################################################

def right_clic(content):
    if re.findall(r"event.button ?== ?2", content):
        return 1
    else:
        return 0


#################################################################################################################################
#              Domain in page title (Shirazi'18)
#################################################################################################################################

def domain_in_title(domain, title):
    if domain.lower() in title.lower(): 
        return 0
    return 1

#################################################################################################################################
#              Domain after copyright logo (Shirazi'18)
#################################################################################################################################

def domain_with_copyright(domain, content):
    try:
        m = re.search(u'(\N{COPYRIGHT SIGN}|\N{TRADE MARK SIGN}|\N{REGISTERED SIGN})', content)
        _copyright = content[m.span()[0]-50:m.span()[0]+50]
        if domain.lower() in _copyright.lower():
            return 0
        else:
            return 1 
    except:
        return 0
