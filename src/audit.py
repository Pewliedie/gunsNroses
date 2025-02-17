import json
import typing as t
from datetime import date, datetime

import sqlalchemy as sa
from sqlalchemy.event import listens_for

import src.models as m
from src.db import session

AUDITED_MODELS = (m.User, m.Case, m.MaterialEvidence, m.MaterialEvidenceEvent)


def json_encoder(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()


def current_session_user() -> m.User | None:
    query = sa.select(m.Session).where(m.Session.active.is_(True))
    current_session = session.scalars(query).first()
    if not current_session:
        return None
    return current_session.user


def create_entry(target, action, connection) -> None:
    changes = {}
    state = sa.inspect(target)
    inspection = sa.inspect(target.__class__)
    _rel_keys = [r.key for r in inspection.relationships]

    for attr in filter(lambda a: a.key not in _rel_keys, state.attrs):
        hist = state.get_history(attr.key, True)

        if action not in ["INSERT"] and not hist.has_changes():
            continue

        added = list(hist.added)
        if hist.unchanged:
            added += list(hist.unchanged)

        changes.update(audit_change_entry(attr.key, added, list(hist.deleted)))

    if not changes:
        return

    current_user = current_session_user()

    params = {
        "object_id": target.id,
        "table_name": target.__table__.name,
        "class_name": target.__class__.__name__,
        "fields": ", ".join(list(changes.keys())),
        "action": action,
        "data": json.dumps(changes, default=json_encoder, ensure_ascii=False),
        "user_id": current_user.id if current_user else None,
    }
    connection.execute(m.AuditEntry.__table__.insert().values(**params))


def audit_change_entry(
    name: str, added: t.Any, deleted: t.Any
) -> dict[str, dict[str, t.Any]]:
    return {name: {"added": added, "deleted": deleted}}


def init_audit():
    for model in AUDITED_MODELS:

        @listens_for(model, "after_insert")
        def receive_after_insert(mapper, connection, target):
            create_entry(target, "INSERT", connection)

        @listens_for(model, "after_update")
        def receive_after_update(mapper, connection, target):
            create_entry(target, "UPDATE", connection)

        @listens_for(model, "after_delete")
        def receive_after_delete(mapper, connection, target):
            create_entry(target, "DELETE", connection)
