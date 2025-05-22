import requests

def main():
    gender = input('Male or Female? ')
    has_job = input('Does he/she has a job? ')
    if has_job[0].lower() == 'y':
        has_job = True
    else:
        has_job = False
    get_name_by_occ_and_gender(gender, has_job)

def get_name_by_occ_and_gender(gender, has_job):
    tallest_supe_by_conds = get_tallest(supe_by_gender(supe_has_job(get_all_supes(), has_job), gender))
    print(tallest_supe_by_conds['name'])


def get_all_supes():
    all_supes = requests.get("https://akabab.github.io/superhero-api/api/all.json")
    if all_supes.status_code == 200:
        return all_supes.json()
    else:
        return "Could not complete request!"

def supe_by_gender(supes, gender):
    gendered_supes = []
    for supe in supes:
        if supe['appearance']['gender'] == gender:
            gendered_supes.append(supe)
    return gendered_supes

def supe_has_job(supes, has_job=True):
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
    tallest_supe = dict()
    tallest_height = 0
    for supe in supes:
        height = float(supe['appearance']['height'][1].split()[0])
        if height > tallest_height:
            tallest_supe = supe
            tallest_heigth = height
    return tallest_supe



if __name__ == "__main__":
    main()
