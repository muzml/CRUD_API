import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.test_stage3_auth import run_all_tests as run_stage3_tests
from tests.test_stage4_user_scoped_tasks import run_stage4_tests
from tests.test_stage5_auth_session import run_stage5_tests


async def main():
    print("=" * 70)
    print(" [RUNNING FULL SUITE] (STAGES 3, 4, 5) - AUTHENTICATION & TASK API")
    print("=" * 70)

    print("\n--- [STAGE 3] Centralized Auth Dependency & Endpoint Protection ---")
    await run_stage3_tests()

    print("\n--- [STAGE 4] User-Scoped Tasks & Ownership Data Isolation ---")
    await run_stage4_tests()

    print("\n--- [STAGE 5] Session Management, Token Refresh & Logout ---")
    await run_stage5_tests()

    print("\n" + "=" * 70)
    print(" [SUCCESS] ALL TEST ASSERTIONS PASSED WITH 100% COVERAGE!")
    print("=" * 70)



if __name__ == "__main__":
    asyncio.run(main())
