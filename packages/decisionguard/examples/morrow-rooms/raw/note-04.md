스탠더드 예약 취소 기능의 수용 조건으로 다음을 승인했다. 24시간 마감선보다 이르면 자동 환불하고, 정확히 그 시각이거나 이후이면 자동 환불하지 않고 검토 대기 상태로 만든다. note-01의 확정된 24시간 정책을 구현하는 조건이다.

For standard-plan booking cancellations, the team approved computing cutoff_at from the room's start time and comparing it with server UTC time on every cancellation request. An earlier price quote cannot authorize a later refund. This design implements the boundary condition in the preceding paragraph and addresses the stale-preview risk described next.

The refund preview can remain open while time passes. This creates an unresolved stale-preview risk for the standard plan: cached eligibility may outlive its cutoff. The server must re-evaluate the request rather than trust the preview.

스탠더드 결제 영수증의 세금 반올림을 한 자리로 바꾸는 안은 초안이다. 예약 취소나 자동 환불의 자격 판정과는 무관한 별도 청구서 작업이다.
