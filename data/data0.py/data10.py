survey_data = {
    "personal_information": {
        "name": "김오순",  # 이름
        "phone": "010-3004-4366",  # 연락처
        "age": 2,  #85세 이상
        "gender": False,  # 여
        "merry": 3,  # 사별
        "living_arrangement": True,  # 혼자 거주
        "number_of_children": 2,  # 3명 이상
        "religion": 0,  # 있다
        "income": 1,  #보통
        "perceived_health_status": 1  # 보통
    },
    "objective_questions": {
        "family_relationship": [
            2,  # 가족과의 대화 시간이 부족하다고 느낀다.
            2,  # 가족과 함께 있는 시간이 충분하지 않다고 생각한다.
            3,  # 가족이 나를 필요로 하지 않는다고 느낀다.
            1   # 가족과 함께 보내는 시간이 즐겁지 않다.
        ],
        "social_loneliness": [
            4,  # 친구와 연락하는 횟수가 줄어들고 있다.
            4,  # 친구와 만나는 시간이 줄어들고 있다.
            4,  # 내가 속한 모임이나 단체에서 소외감을 느낀다.
            3   # 새로운 사람을 만날 기회가 거의 없다.
        ],
        "lack_of_belonging": [
            3,  # 주변 사람들에게 소외감을 느낀다.
            3,  # 내가 중요한 존재라고 느껴지지 않는다.
            2,  # 외출 후에도 혼자 있는 기분이 든다.
            3,  # 누군가와 진심으로 이야기할 기회가 없다.
            4,  # 도움을 요청할 사람이 없다.
            4   # 나의 의견을 들어주는 사람이 없다.
        ]
    },
    "subjective_questions": {
        "loneliness_situations": "외출 후 집에오면 혼자일떄 외로움을 느낀다.",  # 어느 상황에 외로움을 느꼈는지
        "realization_of_loneliness": "외롭다는 느낌이 들고 혼자 밥을 먹을 때 먹기 싫을 때가 많다.",  # 어떻게 외로움을 알아차렸는지
        "needs_during_loneliness": "친구,가족,돈"  # 외로움의 상황에 처해 있을 때 필요한 것이 무엇이라고 생각하는지
    }
}

import json
with open('./survey_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(survey_data, json_file, ensure_ascii=False, indent=4)