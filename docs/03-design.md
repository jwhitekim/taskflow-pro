# 03-design.md (HOW)

| # | 선택 | 대안 | 근거 | 트레이드오프 |
|---|---|---|---|---|
| 1 | 백엔드 - FastAPI | Django, Express | 타입 힌트 기반 자동 검증/문서화, 비동기 지원, 가벼움 | Django 대비 관리자 페이지 등 배터리 미포함 |
| 2 | 프론트 - Vanilla JS + Tailwind CDN | React, Vue | 빌드 도구 없이 즉시 실행, 학습 곡선 최소화. 프론트는 백엔드가 같은 오리진에서 제공하며 file://로 직접 열지 않음 | 컴포넌트화/상태관리 부재로 규모 커지면 유지보수 부담 |
| 3 | DB - SQLite (SQLAlchemy ORM, 추후 PostgreSQL 전환 고려) | PostgreSQL 즉시 도입 | 설치/운영 부담 없이 빠른 개발 가능, ORM으로 전환 경로 확보 | 동시 쓰기 성능/다중 사용자 환경에 취약 |
| 4 | CSS - Tailwind만 (styled-components 금지) | styled-components, CSS Modules | 유틸리티 클래스로 빠른 스타일링, 별도 빌드 불필요 | 클래스 나열로 마크업이 장황해짐 |
| 5 | 실시간 - MVP는 폴링 3초, WebSocket은 확장 단계 보류 | WebSocket 즉시 도입 | 구현/운영 단순, MVP 규모에 충분 | 실시간성 낮고 불필요한 요청 발생 |
| 6 | 상태관리 - 모듈 변수 + DOM 직접 갱신 | Redux, Zustand 등 | 별도 라이브러리 없이 단순 구조 유지 | 상태가 커지면 추적/디버깅 어려움 |
| 7 | 디자인 시스템 - Mac OS UI 톤 | Material, Ant | 제품 톤에 맞는 부드럽고 세련된 인상 | 별도 컴포넌트 라이브러리 없어 직접 구현 필요 |
| 8 | 테마 - 라이트/다크 토글, localStorage, 초기값은 시스템 설정 | 서버 저장, 항상 라이트 고정 | 사용자 선호 유지 + 첫 방문 시 OS 설정 반영 | localStorage 미지원 환경에서는 초기값 유지 불가 |

## 의존성 추가 정책
이 문서에 사유를 적기 전에는 어떤 의존성도 도입할 수 없다.

### 사전 승인 목록
- `httpx` — 테스트 구동에 필요
