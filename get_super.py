import requests

def main():
    print(tallest_by_params()['name'])

def tallest_by_params():
    tallest = get_tallest(supe_by_gender(supe_has_job(get_all_supes())))
    return tallest

def get_all_supes():
    all_supes = requests.get("https://akabab.github.io/superhero-api/api/all.json")
    if all_supes.status_code == 200:
        return all_supes.json()
    else:
        return "Could not complete request!"

def supe_by_gender(supes):
    gender = get_gender()
    gendered_supes = []
    for supe in supes:
        if supe['appearance']['gender'] == gender:
            gendered_supes.append(supe)
    return gendered_supes

def supe_has_job(supes):
    has_job = get_has_job()
    supes_by_job = []
    for supe in supes:
        job = supe['work']['occupation']
        if job == '-':
            job = False
        else:
            job = True
        if has_job == job:
            supes_by_job.append(supe)
    return supes_by_job


def get_tallest(supes):
    tallest_supe = None
    tallest_height = 0
    for supe in supes:
        height = float(supe['appearance']['height'][1].split()[0])
        if height > tallest_height:
            tallest_supe = supe
            tallest_heigth = height
    return tallest_supe

def get_gender():
    gender = input('Male or Female? ').capitalize()
    if gender not in ['Male', 'Female']:
        print('Gender choices: "Male", "Female"')
        raise TypeError
    else:
        return gender

def get_has_job():
    has_job = input('Does he/she has a job? ').lower()
    if has_job not in ['y', 'yes', 'n', 'no']:
        print('Please answer "yes" or "no"')
        raise ValueError
    else:
        if has_job[0].lower() == 'y':
            return True
        else:
            return False

if __name__ == "__main__":
    main()
