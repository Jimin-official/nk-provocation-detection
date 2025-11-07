## map에 보여질 아이콘 관련 함수

# 공통 아이콘 매핑 함수
def get_icon_name(case_name):
    if '핵실험' in case_name:
        return 'bomb'
    elif '미사일' in case_name:
        return 'rocket'
    elif '오물풍선' in case_name:
        return 'circle'
    elif ('피습' in case_name or '천안함' in case_name or '연평도' in case_name or '제2연평' in case_name or '목함지뢰' in case_name):
        return 'user'
    else:
        return 'user'
    
# 색상 매핑
def case_color_map(case_name):
    if '핵실험' in case_name:
        return 'orange'
    elif '미사일' in case_name:
        return 'blue'
    elif '오물풍선' in case_name:
        return 'green'
    elif ('천안함' in case_name or '연평도' in case_name or '제2연평' in case_name or '목함지뢰' in case_name or '피습' in case_name):
        return 'darkred'
    else:
        return 'info-sign'