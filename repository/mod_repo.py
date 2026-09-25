from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import ModerationCase

class ModerationRepository:

    @staticmethod
    async def create_ban(
        session: AsyncSession,
        guild_id: int,
        user_id: int,
        moderator_id: int,
        reason: str | None = None,
    ) -> ModerationCase:

        case_ban = ModerationCase(
            guild_id=guild_id,
            user_id=user_id,
            moderator_id=moderator_id,
            type="BAN",
            reason=reason
        )

        session.add(case_ban)

        await session.flush()

        return case_ban


    @staticmethod
    async def create_kick(
        session: AsyncSession,
        guild_id: int,
        user_id: int,
        moderator_id: int,
        reason: str | None = None
    ) -> ModerationCase:

        case_kick = ModerationCase(
            guild_id=guild_id,
            user_id=user_id,
            moderator_id=moderator_id,
            type="KICK",
            reason=reason
        )

        session.add(case_kick)

        await session.flush()

        return case_kick

    @staticmethod
    async def create_timeout(
        session: AsyncSession,
        guild_id: int,
        user_id: int,
        moderator_id: int,
        reason: str | None = None
    ) -> ModerationCase:

        case_timeout = ModerationCase(
            guild_id=guild_id,
            user_id=user_id,
            moderator_id=moderator_id,
            type="TIMEOUT",
            reason=reason
        )

        session.add(case_timeout)

        await session.flush()

        return case_timeout

    @staticmethod
    async def create_warn(
        session: AsyncSession,
        guild_id: int,
        user_id: int,
        moderator_id: int,
        reason: str | None = None
    ) -> ModerationCase:

        case_warn = ModerationCase(
            guild_id=guild_id,
            user_id=user_id,
            moderator_id=moderator_id,
            type="WARN",
            reason=reason
        )

        session.add(case_warn)
        

        await session.flush()

        return case_warn


    @staticmethod
    async def remove_ban(
        session: AsyncSession,
        guild_id: int,
        user_id: int,
    ) -> ModerationCase | None:

        result = await session.execute(
    select(ModerationCase).where(
        ModerationCase.guild_id == guild_id,
        ModerationCase.user_id == user_id,
        ModerationCase.type == "BAN",
        ModerationCase.active.is_(True)
    )
)

        case_unban = result.scalar_one_or_none()

        if case_unban is None:
            return None

        case_unban.active = False

        await session.flush()

        return case_unban

    @staticmethod
    async def remove_the_timeout(
        session: AsyncSession,
        guild_id: int,
        user_id: int,
    ) -> ModerationCase | None:

        result = await session.execute(
    select(ModerationCase).where(
        ModerationCase.guild_id == guild_id,
        ModerationCase.user_id == user_id,
        ModerationCase.type == "TIMEOUT",
        ModerationCase.active.is_(True)
    )
)

        case_remove_timeout = result.scalar_one_or_none()

        if case_remove_timeout is None:
            return None

        case_remove_timeout.active = False

        await session.flush()

        return case_remove_timeout

    @staticmethod
    async def remove_warn(
        session: AsyncSession,
        guild_id: int,
        user_id: int
    ) -> ModerationCase | None:

        result = await session.execute(select(ModerationCase).where(
            ModerationCase.guild_id == guild_id,
            ModerationCase.user_id == user_id,
            ModerationCase.type == "WARN",
            ModerationCase.active.is_(True)
        ).order_by(ModerationCase.id.desc()).limit(1))

        case_remove_warn = result.scalar_one_or_none()

        if case_remove_warn is None:
            return None

        case_remove_warn.active = False

        await session.flush()

        return case_remove_warn

    @staticmethod
    async def get_user_warns(
        session: AsyncSession,
        guild_id: int,
        user_id: int,
    ) -> ModerationCase | None:

        result = await session.execute(select(ModerationCase).where(
            ModerationCase.guild_id == guild_id,
            ModerationCase.user_id == user_id,
            ModerationCase.type == "WARN",
            ModerationCase.active.is_(True)
        ))

        return list(result.scalars().all())
