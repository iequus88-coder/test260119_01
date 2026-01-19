import streamlit as st
import datetime
import time
import pandas as pd
import random
from PIL import Image

# --------------------------------------------------------------------------
# [설정] 페이지 기본 설정 및 모바일 최적화
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="(주)그랜드썬에스피 안전관리",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------------------------------
# [스타일] CSS 적용 (모바일 폰트, 버튼 크기, 숨김 처리 등)
# --------------------------------------------------------------------------
st.markdown("""
    <style>
    /* 전체 폰트 및 모바일 가독성 조정 */
    html, body, [class*="css"] {
        font-family: 'Pretendard', 'Malgun Gothic', sans-serif;
        font-size: 16px;
    }
    /* 버튼 크기 확대 (터치 편의성) */
    .stButton > button {
        width: 100%;
        height: 3em;
        font-weight: bold;
        border-radius: 10px;
    }
    /* 헤더 숨김 (앱처럼 보이게) */
    header {visibility: hidden;}
    /* 푸터 숨김 */
    footer {visibility: hidden;}
    
    /* 긴급 알림 스타일 */
    .emergency-alert {
        padding: 1rem;
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --------------------------------------------------------------------------
# [데이터] 세션 상태 초기화 (DB 및 NAS 연동 대용)
# --------------------------------------------------------------------------
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'tbm_data' not in st.session_state:
    st.session_state.tbm_data = [] # TBM 데이터 저장소
if 'nas_logs' not in st.session_state:
    st.session_state.nas_logs = [] # NAS 아카이빙 로그

# 모의 기상 데이터 (풍속 10m/s 이상 테스트용)
WIND_SPEED = random.uniform(2.0, 12.0) 

# --------------------------------------------------------------------------
# [함수] 공통 기능 정의 (Interface)
# --------------------------------------------------------------------------

def save_to_nas(site_name, category, content, image=None):
    """
    실제 NAS 서버 연동을 위한 인터페이스입니다.
    현재는 로그를 남기는 것으로 대체합니다.
    경로: \\NAS\Safety_Data\현장명\날짜\
    """
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    path = f"\\\\NAS\\Safety_Data\\{site_name}\\{today}\\"
    
    log_msg = f"[NAS 업로드] 경로: {path} | 분류: {category} | 내용: {content}"
    if image:
        log_msg += " | [사진 첨부됨]"
    
    st.session_state.nas_logs.append(f"{datetime.datetime.now().strftime('%H:%M:%S')} - {log_msg}")
    return True

def go_home():
    st.session_state.page = 'login'

# --------------------------------------------------------------------------
# [UI] 1. 로그인 및 초기 화면
# --------------------------------------------------------------------------
def page_login():
    st.title("☀️ (주)그랜드썬에스피")
    st.subheader("스마트 안전보건 관리 시스템")
    
    # 3D 캐릭터 대용 이미지 (실제 앱에서는 캐릭터 이미지 경로 사용)
    st.info("👋 안녕하세요! 오늘도 안전한 하루 되세요. (안전관리자 똑순이)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👷 관리감독자 업무\n(현장 로그인)"):
            st.session_state.page = 'field_manager'
            st.rerun() # 즉시 리렌더링
            
    with col2:
        if st.button("📊 본사 대시보드\n(관리자용)"):
            st.session_state.page = 'hq_dashboard'
            st.rerun()

    # 산안법 제15조 팝업 (Expander로 구현)
    with st.expander("📜 [필독] 산업안전보건법 제15조 (관리감독자)"):
        st.markdown("""
        **관리감독자의 업무**
        1. 기계/기구 또는 설비의 안전/보건 점검 및 이상 유무 확인
        2. 근로자의 작업복/보호구 및 방호장치의 점검과 그 착용/사용에 관한 교육/지도
        3. 산업재해에 관한 보고 및 이에 대한 응급조치
        4. 작업장 정리/정돈 및 통로 확보에 대한 확인/감독
        """)

    # 홈 화면 추가 가이드
    with st.expander("📲 앱 설치 방법 (홈 화면 추가)"):
        st.write("1. **안드로이드**: 크롬 메뉴(⋮) -> '홈 화면에 추가' 선택")
        st.write("2. **아이폰**: 사파리 공유 버튼(⏏️) -> '홈 화면에 추가' 선택")

# --------------------------------------------------------------------------
# [UI] 2. 현장 책임자 모드 (작업자용)
# --------------------------------------------------------------------------
def page_field_manager():
    st.button("⬅️ 뒤로가기", on_click=go_home)
    st.title("🏗️ 현장 안전 관리")
    
    # 0. 기상 연계 (풍속 체크)
    if WIND_SPEED >= 10.0:
        st.markdown(f"""
        <div class="emergency-alert">
        🚨 경고: 현재 풍속 {WIND_SPEED:.1f}m/s<br>
        전 현장 작업 중지 명령 발동!
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success(f"현재 풍속: {WIND_SPEED:.1f}m/s (작업 가능)")

    # 1. 현장 선택
    site_list = ["경기-안성", "경기-이천", "경기-평택", "경기-여주", "인천", "충청권"]
    selected_site = st.selectbox("현장을 선택하세요", site_list)

    # 탭을 이용한 5대 핵심 메뉴 구현
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🗓️ 작업기간", "✅ TBM", "📄 계획서", "⚠️ 위험보고", "📢 지시사항"])

    # 메뉴 1: 작업 기간
    with tab1:
        st.subheader("공사 기간 확인")
        # 실제 데이터 연동 시 DB에서 가져올 부분
        st.info(f"[{selected_site}] 현장 공사 기간: 2026.01.20 ~ 2026.02.15")

    # 메뉴 2: TBM (안전점검)
    with tab2:
        st.subheader("TBM (Tool Box Meeting)")
        workers = st.text_area("참석자 명단 (콤마로 구분)", "김반장, 이기사, 박작업")
        risk_check = st.checkbox("주요 위험요인 전파 완료")
        tbm_photo = st.file_uploader("TBM 실시 사진 (필수)", type=['jpg', 'png'])
        
        if st.button("TBM 등록 완료"):
            if tbm_photo and risk_check:
                save_to_nas(selected_site, "TBM", f"참석자: {workers}", tbm_photo)
                st.session_state.tbm_data.append({"site": selected_site, "status": "완료"})
                st.success("TBM 내용이 본사 서버로 전송되었습니다.")
            else:
                st.error("사진 업로드 및 위험요인 체크는 필수입니다.")

    # 메뉴 3: 계획서/허가서
    with tab3:
        st.subheader("작업 계획서 승인 요청")
        work_type = st.radio("작업 종류", ["지게차", "크레인", "스카이(고소작업차)"])
        st.file_uploader(f"{work_type} 작업계획서 첨부", type=['pdf', 'jpg'])
        st.button("승인 요청 전송")

    # 메뉴 4: 그 외 위험사항 (Safety Lock 포함)
    with tab4:
        st.subheader("현장 위험 요인 보고")
        st.warning("지붕 작업 시 채광창 보호조치는 필수입니다!")
        
        skylight_photo = st.file_uploader("채광창/위험부위 보호조치 사진", type=['jpg', 'png'], key="skylight")
        
        # Safety Lock 로직
        if skylight_photo:
            st.success("보호조치 확인됨. 작업 시작 버튼이 활성화되었습니다.")
            if st.button("작업 시작 보고"):
                 save_to_nas(selected_site, "위험보고", "채광창 보호조치 완료", skylight_photo)
                 st.info("작업 시작 시간이 기록되었습니다.")
        else:
            st.error("📷 사진을 등록해야 '작업 시작' 버튼이 나타납니다.")

    # 메뉴 5: 본사 지시사항
    with tab5:
        st.subheader("본사 긴급 지시사항")
        st.info("현재 등록된 긴급 지시사항이 없습니다.")
        if st.checkbox("지시사항을 확인하고 이해했습니다."):
            st.write("확인 서명: (자동 입력됨)")

# --------------------------------------------------------------------------
# [UI] 3. 본사 대시보드 모드 (관리자용)
# --------------------------------------------------------------------------
def page_hq_dashboard():
    st.button("⬅️ 로그아웃", on_click=go_home)
    st.title("📊 통합 관제 대시보드")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("오늘 작업 현장", "6 개소")
    col2.metric("TBM 완료율", "83 %", "5/6 완료")
    col3.metric("평균 풍속", f"{WIND_SPEED:.1f} m/s", "-0.5")

    st.markdown("---")
    
    # 현장별 현황 (차트 대용)
    st.subheader("현장별 TBM 현황")
    df = pd.DataFrame({
        "현장": ["경기-안성", "경기-이천", "경기-평택", "충청권"],
        "진행률": [100, 100, 50, 0]
    })
    st.bar_chart(df.set_index("현장"))

    # NAS 아카이빙 로그 (실시간 모니터링)
    st.subheader("🗄️ NAS 실시간 아카이빙 로그")
    log_container = st.container()
    
    with log_container:
        if st.session_state.nas_logs:
            for log in reversed(st.session_state.nas_logs[-5:]): # 최근 5개만
                st.text(log)
        else:
            st.text("아직 데이터가 수집되지 않았습니다.")

    # 긴급 지시 전송
    st.markdown("---")
    st.subheader("🚨 긴급 작업 중지 명령")
    target_site = st.selectbox("대상 현장", ["전체 현장", "경기-안성", "인천"])
    if st.button("긴급 메시지 전송"):
        st.error(f"[{target_site}]에 긴급 메시지가 발송되었습니다.")

# --------------------------------------------------------------------------
# [메인] 페이지 라우팅
# --------------------------------------------------------------------------
def main():
    if st.session_state.page == 'login':
        page_login()
    elif st.session_state.page == 'field_manager':
        page_field_manager()
    elif st.session_state.page == 'hq_dashboard':
        page_hq_dashboard()

if __name__ == "__main__":
    main()
