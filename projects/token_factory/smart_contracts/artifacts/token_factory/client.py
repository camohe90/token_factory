# flake8: noqa
# fmt: off
# mypy: disable-error-code="no-any-return, no-untyped-call, misc, type-arg"
# This file was automatically generated by algokit-client-generator.
# DO NOT MODIFY IT BY HAND.
# requires: algokit-utils@^1.2.0
import base64
import dataclasses
import decimal
import typing
from abc import ABC, abstractmethod

import algokit_utils
import algosdk
from algosdk.v2client import models
from algosdk.atomic_transaction_composer import (
    AtomicTransactionComposer,
    AtomicTransactionResponse,
    SimulateAtomicTransactionResponse,
    TransactionSigner,
    TransactionWithSigner
)

_APP_SPEC_JSON = r"""{
    "hints": {
        "create_asset(string,string)void": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "set_price(uint64)void": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "sell_asset(pay,uint64)void": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "get_asset_id()uint64": {
            "call_config": {
                "no_op": "CALL"
            }
        }
    },
    "source": {
        "approval": "I3ByYWdtYSB2ZXJzaW9uIDEwCgpzbWFydF9jb250cmFjdHMudG9rZW5fZmFjdG9yeS5jb250cmFjdC5Ub2tlbkZhY3RvcnkuYXBwcm92YWxfcHJvZ3JhbToKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy90b2tlbl9mYWN0b3J5L2NvbnRyYWN0LnB5OjQKICAgIC8vIGNsYXNzIFRva2VuRmFjdG9yeShBUkM0Q29udHJhY3QpOgogICAgdHhuIE51bUFwcEFyZ3MKICAgIGJ6IG1haW5fYmFyZV9yb3V0aW5nQDgKICAgIG1ldGhvZCAiY3JlYXRlX2Fzc2V0KHN0cmluZyxzdHJpbmcpdm9pZCIKICAgIG1ldGhvZCAic2V0X3ByaWNlKHVpbnQ2NCl2b2lkIgogICAgbWV0aG9kICJzZWxsX2Fzc2V0KHBheSx1aW50NjQpdm9pZCIKICAgIG1ldGhvZCAiZ2V0X2Fzc2V0X2lkKCl1aW50NjQiCiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyAwCiAgICBtYXRjaCBtYWluX2NyZWF0ZV9hc3NldF9yb3V0ZUAyIG1haW5fc2V0X3ByaWNlX3JvdXRlQDMgbWFpbl9zZWxsX2Fzc2V0X3JvdXRlQDQgbWFpbl9nZXRfYXNzZXRfaWRfcm91dGVANQogICAgZXJyIC8vIHJlamVjdCB0cmFuc2FjdGlvbgoKbWFpbl9jcmVhdGVfYXNzZXRfcm91dGVAMjoKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy90b2tlbl9mYWN0b3J5L2NvbnRyYWN0LnB5OjgKICAgIC8vIEBhcmM0LmFiaW1ldGhvZCgpCiAgICB0eG4gT25Db21wbGV0aW9uCiAgICAhCiAgICBhc3NlcnQgLy8gT25Db21wbGV0aW9uIGlzIE5vT3AKICAgIHR4biBBcHBsaWNhdGlvbklECiAgICBhc3NlcnQgLy8gaXMgbm90IGNyZWF0aW5nCiAgICAvLyBzbWFydF9jb250cmFjdHMvdG9rZW5fZmFjdG9yeS9jb250cmFjdC5weTo0CiAgICAvLyBjbGFzcyBUb2tlbkZhY3RvcnkoQVJDNENvbnRyYWN0KToKICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDEKICAgIGV4dHJhY3QgMiAwCiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyAyCiAgICBleHRyYWN0IDIgMAogICAgLy8gc21hcnRfY29udHJhY3RzL3Rva2VuX2ZhY3RvcnkvY29udHJhY3QucHk6OAogICAgLy8gQGFyYzQuYWJpbWV0aG9kKCkKICAgIGNhbGxzdWIgY3JlYXRlX2Fzc2V0CiAgICBpbnQgMQogICAgcmV0dXJuCgptYWluX3NldF9wcmljZV9yb3V0ZUAzOgogICAgLy8gc21hcnRfY29udHJhY3RzL3Rva2VuX2ZhY3RvcnkvY29udHJhY3QucHk6MTkKICAgIC8vIEBhcmM0LmFiaW1ldGhvZCgpCiAgICB0eG4gT25Db21wbGV0aW9uCiAgICAhCiAgICBhc3NlcnQgLy8gT25Db21wbGV0aW9uIGlzIE5vT3AKICAgIHR4biBBcHBsaWNhdGlvbklECiAgICBhc3NlcnQgLy8gaXMgbm90IGNyZWF0aW5nCiAgICAvLyBzbWFydF9jb250cmFjdHMvdG9rZW5fZmFjdG9yeS9jb250cmFjdC5weTo0CiAgICAvLyBjbGFzcyBUb2tlbkZhY3RvcnkoQVJDNENvbnRyYWN0KToKICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDEKICAgIGJ0b2kKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy90b2tlbl9mYWN0b3J5L2NvbnRyYWN0LnB5OjE5CiAgICAvLyBAYXJjNC5hYmltZXRob2QoKQogICAgY2FsbHN1YiBzZXRfcHJpY2UKICAgIGludCAxCiAgICByZXR1cm4KCm1haW5fc2VsbF9hc3NldF9yb3V0ZUA0OgogICAgLy8gc21hcnRfY29udHJhY3RzL3Rva2VuX2ZhY3RvcnkvY29udHJhY3QucHk6MjQKICAgIC8vIEBhcmM0LmFiaW1ldGhvZCgpCiAgICB0eG4gT25Db21wbGV0aW9uCiAgICAhCiAgICBhc3NlcnQgLy8gT25Db21wbGV0aW9uIGlzIE5vT3AKICAgIHR4biBBcHBsaWNhdGlvbklECiAgICBhc3NlcnQgLy8gaXMgbm90IGNyZWF0aW5nCiAgICAvLyBzbWFydF9jb250cmFjdHMvdG9rZW5fZmFjdG9yeS9jb250cmFjdC5weTo0CiAgICAvLyBjbGFzcyBUb2tlbkZhY3RvcnkoQVJDNENvbnRyYWN0KToKICAgIHR4biBHcm91cEluZGV4CiAgICBpbnQgMQogICAgLQogICAgZHVwCiAgICBndHhucyBUeXBlRW51bQogICAgaW50IHBheQogICAgPT0KICAgIGFzc2VydCAvLyB0cmFuc2FjdGlvbiB0eXBlIGlzIHBheQogICAgdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMQogICAgYnRvaQogICAgLy8gc21hcnRfY29udHJhY3RzL3Rva2VuX2ZhY3RvcnkvY29udHJhY3QucHk6MjQKICAgIC8vIEBhcmM0LmFiaW1ldGhvZCgpCiAgICBjYWxsc3ViIHNlbGxfYXNzZXQKICAgIGludCAxCiAgICByZXR1cm4KCm1haW5fZ2V0X2Fzc2V0X2lkX3JvdXRlQDU6CiAgICAvLyBzbWFydF9jb250cmFjdHMvdG9rZW5fZmFjdG9yeS9jb250cmFjdC5weTozNwogICAgLy8gQGFyYzQuYWJpbWV0aG9kCiAgICB0eG4gT25Db21wbGV0aW9uCiAgICAhCiAgICBhc3NlcnQgLy8gT25Db21wbGV0aW9uIGlzIE5vT3AKICAgIHR4biBBcHBsaWNhdGlvbklECiAgICBhc3NlcnQgLy8gaXMgbm90IGNyZWF0aW5nCiAgICBjYWxsc3ViIGdldF9hc3NldF9pZAogICAgaXRvYgogICAgYnl0ZSAweDE1MWY3Yzc1CiAgICBzd2FwCiAgICBjb25jYXQKICAgIGxvZwogICAgaW50IDEKICAgIHJldHVybgoKbWFpbl9iYXJlX3JvdXRpbmdAODoKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy90b2tlbl9mYWN0b3J5L2NvbnRyYWN0LnB5OjQKICAgIC8vIGNsYXNzIFRva2VuRmFjdG9yeShBUkM0Q29udHJhY3QpOgogICAgdHhuIE9uQ29tcGxldGlvbgogICAgIQogICAgYXNzZXJ0IC8vIHJlamVjdCB0cmFuc2FjdGlvbgogICAgdHhuIEFwcGxpY2F0aW9uSUQKICAgICEKICAgIGFzc2VydCAvLyBpcyBjcmVhdGluZwogICAgaW50IDEKICAgIHJldHVybgoKCi8vIHNtYXJ0X2NvbnRyYWN0cy50b2tlbl9mYWN0b3J5LmNvbnRyYWN0LlRva2VuRmFjdG9yeS5jcmVhdGVfYXNzZXQoYXNzZXRfbmFtZTogYnl0ZXMsIHVuaXRfbmFtZTogYnl0ZXMpIC0+IHZvaWQ6CmNyZWF0ZV9hc3NldDoKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy90b2tlbl9mYWN0b3J5L2NvbnRyYWN0LnB5OjgtOQogICAgLy8gQGFyYzQuYWJpbWV0aG9kKCkKICAgIC8vIGRlZiBjcmVhdGVfYXNzZXQoc2VsZiwgYXNzZXRfbmFtZTpTdHJpbmcsIHVuaXRfbmFtZTpTdHJpbmcpIC0+Tm9uZToKICAgIHByb3RvIDIgMAogICAgLy8gc21hcnRfY29udHJhY3RzL3Rva2VuX2ZhY3RvcnkvY29udHJhY3QucHk6MTAtMTYKICAgIC8vIHNlbGYuYXNzZXRfY3JlYXRlZCA9IGl0eG4uQXNzZXRDb25maWcgKAogICAgLy8gICAgIGFzc2V0X25hbWU9IGFzc2V0X25hbWUsCiAgICAvLyAgICAgdW5pdF9uYW1lPSB1bml0X25hbWUsCiAgICAvLyAgICAgdG90YWw9IDEwXzAwMCwKICAgIC8vICAgICBkZWNpbWFscz0gMSwKICAgIC8vICAgICBkZWZhdWx0X2Zyb3plbj1GYWxzZQogICAgLy8gKS5zdWJtaXQoKS5jcmVhdGVkX2Fzc2V0LmlkCiAgICBpdHhuX2JlZ2luCiAgICAvLyBzbWFydF9jb250cmFjdHMvdG9rZW5fZmFjdG9yeS9jb250cmFjdC5weToxNQogICAgLy8gZGVmYXVsdF9mcm96ZW49RmFsc2UKICAgIGludCAwCiAgICBpdHhuX2ZpZWxkIENvbmZpZ0Fzc2V0RGVmYXVsdEZyb3plbgogICAgLy8gc21hcnRfY29udHJhY3RzL3Rva2VuX2ZhY3RvcnkvY29udHJhY3QucHk6MTQKICAgIC8vIGRlY2ltYWxzPSAxLAogICAgaW50IDEKICAgIGl0eG5fZmllbGQgQ29uZmlnQXNzZXREZWNpbWFscwogICAgLy8gc21hcnRfY29udHJhY3RzL3Rva2VuX2ZhY3RvcnkvY29udHJhY3QucHk6MTMKICAgIC8vIHRvdGFsPSAxMF8wMDAsCiAgICBpbnQgMTAwMDAKICAgIGl0eG5fZmllbGQgQ29uZmlnQXNzZXRUb3RhbAogICAgZnJhbWVfZGlnIC0xCiAgICBpdHhuX2ZpZWxkIENvbmZpZ0Fzc2V0VW5pdE5hbWUKICAgIGZyYW1lX2RpZyAtMgogICAgaXR4bl9maWVsZCBDb25maWdBc3NldE5hbWUKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy90b2tlbl9mYWN0b3J5L2NvbnRyYWN0LnB5OjEwCiAgICAvLyBzZWxmLmFzc2V0X2NyZWF0ZWQgPSBpdHhuLkFzc2V0Q29uZmlnICgKICAgIGludCBhY2ZnCiAgICBpdHhuX2ZpZWxkIFR5cGVFbnVtCiAgICBpbnQgMAogICAgaXR4bl9maWVsZCBGZWUKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy90b2tlbl9mYWN0b3J5L2NvbnRyYWN0LnB5OjEwLTE2CiAgICAvLyBzZWxmLmFzc2V0X2NyZWF0ZWQgPSBpdHhuLkFzc2V0Q29uZmlnICgKICAgIC8vICAgICBhc3NldF9uYW1lPSBhc3NldF9uYW1lLAogICAgLy8gICAgIHVuaXRfbmFtZT0gdW5pdF9uYW1lLAogICAgLy8gICAgIHRvdGFsPSAxMF8wMDAsCiAgICAvLyAgICAgZGVjaW1hbHM9IDEsCiAgICAvLyAgICAgZGVmYXVsdF9mcm96ZW49RmFsc2UKICAgIC8vICkuc3VibWl0KCkuY3JlYXRlZF9hc3NldC5pZAogICAgaXR4bl9zdWJtaXQKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy90b2tlbl9mYWN0b3J5L2NvbnRyYWN0LnB5OjEwCiAgICAvLyBzZWxmLmFzc2V0X2NyZWF0ZWQgPSBpdHhuLkFzc2V0Q29uZmlnICgKICAgIGJ5dGUgImFzc2V0X2NyZWF0ZWQiCiAgICAvLyBzbWFydF9jb250cmFjdHMvdG9rZW5fZmFjdG9yeS9jb250cmFjdC5weToxMC0xNgogICAgLy8gc2VsZi5hc3NldF9jcmVhdGVkID0gaXR4bi5Bc3NldENvbmZpZyAoCiAgICAvLyAgICAgYXNzZXRfbmFtZT0gYXNzZXRfbmFtZSwKICAgIC8vICAgICB1bml0X25hbWU9IHVuaXRfbmFtZSwKICAgIC8vICAgICB0b3RhbD0gMTBfMDAwLAogICAgLy8gICAgIGRlY2ltYWxzPSAxLAogICAgLy8gICAgIGRlZmF1bHRfZnJvemVuPUZhbHNlCiAgICAvLyApLnN1Ym1pdCgpLmNyZWF0ZWRfYXNzZXQuaWQKICAgIGl0eG4gQ3JlYXRlZEFzc2V0SUQKICAgIGFwcF9nbG9iYWxfcHV0CiAgICByZXRzdWIKCgovLyBzbWFydF9jb250cmFjdHMudG9rZW5fZmFjdG9yeS5jb250cmFjdC5Ub2tlbkZhY3Rvcnkuc2V0X3ByaWNlKHVuaXRhcnlfcHJpY2U6IHVpbnQ2NCkgLT4gdm9pZDoKc2V0X3ByaWNlOgogICAgLy8gc21hcnRfY29udHJhY3RzL3Rva2VuX2ZhY3RvcnkvY29udHJhY3QucHk6MTktMjAKICAgIC8vIEBhcmM0LmFiaW1ldGhvZCgpCiAgICAvLyBkZWYgc2V0X3ByaWNlKHNlbGYsIHVuaXRhcnlfcHJpY2U6VUludDY0KS0+Tm9uZToKICAgIHByb3RvIDEgMAogICAgLy8gc21hcnRfY29udHJhY3RzL3Rva2VuX2ZhY3RvcnkvY29udHJhY3QucHk6MjEKICAgIC8vIGFzc2VydCBUeG4uc2VuZGVyID09IEdsb2JhbC5jcmVhdG9yX2FkZHJlc3MKICAgIHR4biBTZW5kZXIKICAgIGdsb2JhbCBDcmVhdG9yQWRkcmVzcwogICAgPT0KICAgIGFzc2VydAogICAgLy8gc21hcnRfY29udHJhY3RzL3Rva2VuX2ZhY3RvcnkvY29udHJhY3QucHk6MjIKICAgIC8vIHNlbGYudW5pdGFyeV9wcmljZSA9IHVuaXRhcnlfcHJpY2UKICAgIGJ5dGUgInVuaXRhcnlfcHJpY2UiCiAgICBmcmFtZV9kaWcgLTEKICAgIGFwcF9nbG9iYWxfcHV0CiAgICByZXRzdWIKCgovLyBzbWFydF9jb250cmFjdHMudG9rZW5fZmFjdG9yeS5jb250cmFjdC5Ub2tlbkZhY3Rvcnkuc2VsbF9hc3NldChidXllcl90eG46IHVpbnQ2NCwgcXVhbnRpdHk6IHVpbnQ2NCkgLT4gdm9pZDoKc2VsbF9hc3NldDoKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy90b2tlbl9mYWN0b3J5L2NvbnRyYWN0LnB5OjI0LTI1CiAgICAvLyBAYXJjNC5hYmltZXRob2QoKQogICAgLy8gZGVmIHNlbGxfYXNzZXQoc2VsZiwgYnV5ZXJfdHhuOiBndHhuLlBheW1lbnRUcmFuc2FjdGlvbiwgcXVhbnRpdHk6IFVJbnQ2NCkgLT5Ob25lOgogICAgcHJvdG8gMiAwCiAgICAvLyBzbWFydF9jb250cmFjdHMvdG9rZW5fZmFjdG9yeS9jb250cmFjdC5weToyNgogICAgLy8gYXNzZXJ0IGJ1eWVyX3R4bi5zZW5kZXIgPT0gVHhuLnNlbmRlcgogICAgZnJhbWVfZGlnIC0yCiAgICBndHhucyBTZW5kZXIKICAgIHR4biBTZW5kZXIKICAgID09CiAgICBhc3NlcnQKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy90b2tlbl9mYWN0b3J5L2NvbnRyYWN0LnB5OjI3CiAgICAvLyBhc3NlcnQgYnV5ZXJfdHhuLnJlY2VpdmVyID09IEdsb2JhbC5jdXJyZW50X2FwcGxpY2F0aW9uX2FkZHJlc3MKICAgIGZyYW1lX2RpZyAtMgogICAgZ3R4bnMgUmVjZWl2ZXIKICAgIGdsb2JhbCBDdXJyZW50QXBwbGljYXRpb25BZGRyZXNzCiAgICA9PQogICAgYXNzZXJ0CiAgICAvLyBzbWFydF9jb250cmFjdHMvdG9rZW5fZmFjdG9yeS9jb250cmFjdC5weToyOAogICAgLy8gYXNzZXJ0IGJ1eWVyX3R4bi5hbW91bnQgPT0gc2VsZi51bml0YXJ5X3ByaWNlICogcXVhbnRpdHkKICAgIGZyYW1lX2RpZyAtMgogICAgZ3R4bnMgQW1vdW50CiAgICBpbnQgMAogICAgYnl0ZSAidW5pdGFyeV9wcmljZSIKICAgIGFwcF9nbG9iYWxfZ2V0X2V4CiAgICBhc3NlcnQgLy8gY2hlY2sgdW5pdGFyeV9wcmljZSBleGlzdHMKICAgIGZyYW1lX2RpZyAtMQogICAgKgogICAgPT0KICAgIGFzc2VydAogICAgLy8gc21hcnRfY29udHJhY3RzL3Rva2VuX2ZhY3RvcnkvY29udHJhY3QucHk6MzAtMzQKICAgIC8vIGl0eG4uQXNzZXRUcmFuc2ZlcigKICAgIC8vICAgICB4ZmVyX2Fzc2V0PXNlbGYuYXNzZXRfY3JlYXRlZCwKICAgIC8vICAgICBhc3NldF9yZWNlaXZlcj0gVHhuLnNlbmRlciwKICAgIC8vICAgICBhc3NldF9hbW91bnQ9cXVhbnRpdHkKICAgIC8vICkuc3VibWl0KCkKICAgIGl0eG5fYmVnaW4KICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy90b2tlbl9mYWN0b3J5L2NvbnRyYWN0LnB5OjMxCiAgICAvLyB4ZmVyX2Fzc2V0PXNlbGYuYXNzZXRfY3JlYXRlZCwKICAgIGludCAwCiAgICBieXRlICJhc3NldF9jcmVhdGVkIgogICAgYXBwX2dsb2JhbF9nZXRfZXgKICAgIGFzc2VydCAvLyBjaGVjayBhc3NldF9jcmVhdGVkIGV4aXN0cwogICAgLy8gc21hcnRfY29udHJhY3RzL3Rva2VuX2ZhY3RvcnkvY29udHJhY3QucHk6MzIKICAgIC8vIGFzc2V0X3JlY2VpdmVyPSBUeG4uc2VuZGVyLAogICAgdHhuIFNlbmRlcgogICAgZnJhbWVfZGlnIC0xCiAgICBpdHhuX2ZpZWxkIEFzc2V0QW1vdW50CiAgICBpdHhuX2ZpZWxkIEFzc2V0UmVjZWl2ZXIKICAgIGl0eG5fZmllbGQgWGZlckFzc2V0CiAgICAvLyBzbWFydF9jb250cmFjdHMvdG9rZW5fZmFjdG9yeS9jb250cmFjdC5weTozMAogICAgLy8gaXR4bi5Bc3NldFRyYW5zZmVyKAogICAgaW50IGF4ZmVyCiAgICBpdHhuX2ZpZWxkIFR5cGVFbnVtCiAgICBpbnQgMAogICAgaXR4bl9maWVsZCBGZWUKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy90b2tlbl9mYWN0b3J5L2NvbnRyYWN0LnB5OjMwLTM0CiAgICAvLyBpdHhuLkFzc2V0VHJhbnNmZXIoCiAgICAvLyAgICAgeGZlcl9hc3NldD1zZWxmLmFzc2V0X2NyZWF0ZWQsCiAgICAvLyAgICAgYXNzZXRfcmVjZWl2ZXI9IFR4bi5zZW5kZXIsCiAgICAvLyAgICAgYXNzZXRfYW1vdW50PXF1YW50aXR5CiAgICAvLyApLnN1Ym1pdCgpCiAgICBpdHhuX3N1Ym1pdAogICAgcmV0c3ViCgoKLy8gc21hcnRfY29udHJhY3RzLnRva2VuX2ZhY3RvcnkuY29udHJhY3QuVG9rZW5GYWN0b3J5LmdldF9hc3NldF9pZCgpIC0+IHVpbnQ2NDoKZ2V0X2Fzc2V0X2lkOgogICAgLy8gc21hcnRfY29udHJhY3RzL3Rva2VuX2ZhY3RvcnkvY29udHJhY3QucHk6MzctMzgKICAgIC8vIEBhcmM0LmFiaW1ldGhvZAogICAgLy8gZGVmIGdldF9hc3NldF9pZChzZWxmKS0+IFVJbnQ2NDoKICAgIHByb3RvIDAgMQogICAgLy8gc21hcnRfY29udHJhY3RzL3Rva2VuX2ZhY3RvcnkvY29udHJhY3QucHk6MzkKICAgIC8vIHJldHVybiBzZWxmLmFzc2V0X2NyZWF0ZWQKICAgIGludCAwCiAgICBieXRlICJhc3NldF9jcmVhdGVkIgogICAgYXBwX2dsb2JhbF9nZXRfZXgKICAgIGFzc2VydCAvLyBjaGVjayBhc3NldF9jcmVhdGVkIGV4aXN0cwogICAgcmV0c3ViCg==",
        "clear": "I3ByYWdtYSB2ZXJzaW9uIDEwCgpzbWFydF9jb250cmFjdHMudG9rZW5fZmFjdG9yeS5jb250cmFjdC5Ub2tlbkZhY3RvcnkuY2xlYXJfc3RhdGVfcHJvZ3JhbToKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy90b2tlbl9mYWN0b3J5L2NvbnRyYWN0LnB5OjQKICAgIC8vIGNsYXNzIFRva2VuRmFjdG9yeShBUkM0Q29udHJhY3QpOgogICAgaW50IDEKICAgIHJldHVybgo="
    },
    "state": {
        "global": {
            "num_byte_slices": 0,
            "num_uints": 3
        },
        "local": {
            "num_byte_slices": 0,
            "num_uints": 0
        }
    },
    "schema": {
        "global": {
            "declared": {
                "asset_created": {
                    "type": "uint64",
                    "key": "asset_created"
                },
                "asset_id": {
                    "type": "uint64",
                    "key": "asset_id"
                },
                "unitary_price": {
                    "type": "uint64",
                    "key": "unitary_price"
                }
            },
            "reserved": {}
        },
        "local": {
            "declared": {},
            "reserved": {}
        }
    },
    "contract": {
        "name": "TokenFactory",
        "methods": [
            {
                "name": "create_asset",
                "args": [
                    {
                        "type": "string",
                        "name": "asset_name"
                    },
                    {
                        "type": "string",
                        "name": "unit_name"
                    }
                ],
                "returns": {
                    "type": "void"
                }
            },
            {
                "name": "set_price",
                "args": [
                    {
                        "type": "uint64",
                        "name": "unitary_price"
                    }
                ],
                "returns": {
                    "type": "void"
                }
            },
            {
                "name": "sell_asset",
                "args": [
                    {
                        "type": "pay",
                        "name": "buyer_txn"
                    },
                    {
                        "type": "uint64",
                        "name": "quantity"
                    }
                ],
                "returns": {
                    "type": "void"
                }
            },
            {
                "name": "get_asset_id",
                "args": [],
                "returns": {
                    "type": "uint64"
                }
            }
        ],
        "networks": {}
    },
    "bare_call_config": {
        "no_op": "CREATE"
    }
}"""
APP_SPEC = algokit_utils.ApplicationSpecification.from_json(_APP_SPEC_JSON)
_TReturn = typing.TypeVar("_TReturn")


class _ArgsBase(ABC, typing.Generic[_TReturn]):
    @staticmethod
    @abstractmethod
    def method() -> str:
        ...


_TArgs = typing.TypeVar("_TArgs", bound=_ArgsBase[typing.Any])


@dataclasses.dataclass(kw_only=True)
class _TArgsHolder(typing.Generic[_TArgs]):
    args: _TArgs


def _filter_none(value: dict | typing.Any) -> dict | typing.Any:
    if isinstance(value, dict):
        return {k: _filter_none(v) for k, v in value.items() if v is not None}
    return value


def _as_dict(data: typing.Any, *, convert_all: bool = True) -> dict[str, typing.Any]:
    if data is None:
        return {}
    if not dataclasses.is_dataclass(data):
        raise TypeError(f"{data} must be a dataclass")
    if convert_all:
        result = dataclasses.asdict(data)
    else:
        result = {f.name: getattr(data, f.name) for f in dataclasses.fields(data)}
    return _filter_none(result)


def _convert_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.TransactionParametersDict:
    return typing.cast(algokit_utils.TransactionParametersDict, _as_dict(transaction_parameters))


def _convert_call_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.OnCompleteCallParametersDict:
    return typing.cast(algokit_utils.OnCompleteCallParametersDict, _as_dict(transaction_parameters))


def _convert_create_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
    on_complete: algokit_utils.OnCompleteActionName,
) -> algokit_utils.CreateCallParametersDict:
    result = typing.cast(algokit_utils.CreateCallParametersDict, _as_dict(transaction_parameters))
    on_complete_enum = on_complete.replace("_", " ").title().replace(" ", "") + "OC"
    result["on_complete"] = getattr(algosdk.transaction.OnComplete, on_complete_enum)
    return result


def _convert_deploy_args(
    deploy_args: algokit_utils.DeployCallArgs | None,
) -> algokit_utils.ABICreateCallArgsDict | None:
    if deploy_args is None:
        return None

    deploy_args_dict = typing.cast(algokit_utils.ABICreateCallArgsDict, _as_dict(deploy_args))
    if isinstance(deploy_args, _TArgsHolder):
        deploy_args_dict["args"] = _as_dict(deploy_args.args)
        deploy_args_dict["method"] = deploy_args.args.method()

    return deploy_args_dict


@dataclasses.dataclass(kw_only=True)
class CreateAssetArgs(_ArgsBase[None]):
    asset_name: str
    unit_name: str

    @staticmethod
    def method() -> str:
        return "create_asset(string,string)void"


@dataclasses.dataclass(kw_only=True)
class SetPriceArgs(_ArgsBase[None]):
    unitary_price: int

    @staticmethod
    def method() -> str:
        return "set_price(uint64)void"


@dataclasses.dataclass(kw_only=True)
class SellAssetArgs(_ArgsBase[None]):
    buyer_txn: TransactionWithSigner
    quantity: int

    @staticmethod
    def method() -> str:
        return "sell_asset(pay,uint64)void"


@dataclasses.dataclass(kw_only=True)
class GetAssetIdArgs(_ArgsBase[int]):
    @staticmethod
    def method() -> str:
        return "get_asset_id()uint64"


class GlobalState:
    def __init__(self, data: dict[bytes, bytes | int]):
        self.asset_created = typing.cast(int, data.get(b"asset_created"))
        self.asset_id = typing.cast(int, data.get(b"asset_id"))
        self.unitary_price = typing.cast(int, data.get(b"unitary_price"))


@dataclasses.dataclass(kw_only=True)
class SimulateOptions:
    allow_more_logs: bool = dataclasses.field(default=False)
    allow_empty_signatures: bool = dataclasses.field(default=False)
    extra_opcode_budget: int = dataclasses.field(default=0)
    exec_trace_config: models.SimulateTraceConfig | None         = dataclasses.field(default=None)


class Composer:

    def __init__(self, app_client: algokit_utils.ApplicationClient, atc: AtomicTransactionComposer):
        self.app_client = app_client
        self.atc = atc

    def build(self) -> AtomicTransactionComposer:
        return self.atc

    def simulate(self, options: SimulateOptions | None = None) -> SimulateAtomicTransactionResponse:
        request = models.SimulateRequest(
            allow_more_logs=options.allow_more_logs,
            allow_empty_signatures=options.allow_empty_signatures,
            extra_opcode_budget=options.extra_opcode_budget,
            exec_trace_config=options.exec_trace_config,
            txn_groups=[]
        ) if options else None
        result = self.atc.simulate(self.app_client.algod_client, request)
        return result

    def execute(self) -> AtomicTransactionResponse:
        return self.app_client.execute_atc(self.atc)

    def create_asset(
        self,
        *,
        asset_name: str,
        unit_name: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `create_asset(string,string)void` ABI method
        
        :param str asset_name: The `asset_name` ABI parameter
        :param str unit_name: The `unit_name` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = CreateAssetArgs(
            asset_name=asset_name,
            unit_name=unit_name,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def set_price(
        self,
        *,
        unitary_price: int,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `set_price(uint64)void` ABI method
        
        :param int unitary_price: The `unitary_price` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = SetPriceArgs(
            unitary_price=unitary_price,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def sell_asset(
        self,
        *,
        buyer_txn: TransactionWithSigner,
        quantity: int,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `sell_asset(pay,uint64)void` ABI method
        
        :param TransactionWithSigner buyer_txn: The `buyer_txn` ABI parameter
        :param int quantity: The `quantity` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = SellAssetArgs(
            buyer_txn=buyer_txn,
            quantity=quantity,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def get_asset_id(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `get_asset_id()uint64` ABI method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = GetAssetIdArgs()
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def create_bare(
        self,
        *,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to create an application using the no_op bare method
        
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        self.app_client.compose_create(
            self.atc,
            call_abi_method=False,
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
        )
        return self

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> "Composer":
        """Adds a call to the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass"""
    
        self.app_client.compose_clear_state(self.atc, _convert_transaction_parameters(transaction_parameters), app_args)
        return self


class TokenFactoryClient:
    """A class for interacting with the TokenFactory app providing high productivity and
    strongly typed methods to deploy and call the app"""

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        ...

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        ...

    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account | None = None,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        """
        TokenFactoryClient can be created with an app_id to interact with an existing application, alternatively
        it can be created with a creator and indexer_client specified to find existing applications by name and creator.
        
        :param AlgodClient algod_client: AlgoSDK algod client
        :param int app_id: The app_id of an existing application, to instead find the application by creator and name
        use the creator and indexer_client parameters
        :param str | Account creator: The address or Account of the app creator to resolve the app_id
        :param IndexerClient indexer_client: AlgoSDK indexer client, only required if deploying or finding app_id by
        creator and app name
        :param AppLookup existing_deployments:
        :param TransactionSigner | Account signer: Account or signer to use to sign transactions, if not specified and
        creator was passed as an Account will use that.
        :param str sender: Address to use as the sender for all transactions, will use the address associated with the
        signer if not specified.
        :param TemplateValueMapping template_values: Values to use for TMPL_* template variables, dictionary keys should
        *NOT* include the TMPL_ prefix
        :param str | None app_name: Name of application to use when deploying, defaults to name defined on the
        Application Specification
            """

        self.app_spec = APP_SPEC
        
        # calling full __init__ signature, so ignoring mypy warning about overloads
        self.app_client = algokit_utils.ApplicationClient(  # type: ignore[call-overload, misc]
            algod_client=algod_client,
            app_spec=self.app_spec,
            app_id=app_id,
            creator=creator,
            indexer_client=indexer_client,
            existing_deployments=existing_deployments,
            signer=signer,
            sender=sender,
            suggested_params=suggested_params,
            template_values=template_values,
            app_name=app_name,
        )

    @property
    def algod_client(self) -> algosdk.v2client.algod.AlgodClient:
        return self.app_client.algod_client

    @property
    def app_id(self) -> int:
        return self.app_client.app_id

    @app_id.setter
    def app_id(self, value: int) -> None:
        self.app_client.app_id = value

    @property
    def app_address(self) -> str:
        return self.app_client.app_address

    @property
    def sender(self) -> str | None:
        return self.app_client.sender

    @sender.setter
    def sender(self, value: str) -> None:
        self.app_client.sender = value

    @property
    def signer(self) -> TransactionSigner | None:
        return self.app_client.signer

    @signer.setter
    def signer(self, value: TransactionSigner) -> None:
        self.app_client.signer = value

    @property
    def suggested_params(self) -> algosdk.transaction.SuggestedParams | None:
        return self.app_client.suggested_params

    @suggested_params.setter
    def suggested_params(self, value: algosdk.transaction.SuggestedParams | None) -> None:
        self.app_client.suggested_params = value

    def get_global_state(self) -> GlobalState:
        """Returns the application's global state wrapped in a strongly typed class with options to format the stored value"""

        state = typing.cast(dict[bytes, bytes | int], self.app_client.get_global_state(raw=True))
        return GlobalState(state)

    def create_asset(
        self,
        *,
        asset_name: str,
        unit_name: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        """Calls `create_asset(string,string)void` ABI method
        
        :param str asset_name: The `asset_name` ABI parameter
        :param str unit_name: The `unit_name` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[None]: The result of the transaction"""

        args = CreateAssetArgs(
            asset_name=asset_name,
            unit_name=unit_name,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def set_price(
        self,
        *,
        unitary_price: int,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        """Calls `set_price(uint64)void` ABI method
        
        :param int unitary_price: The `unitary_price` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[None]: The result of the transaction"""

        args = SetPriceArgs(
            unitary_price=unitary_price,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def sell_asset(
        self,
        *,
        buyer_txn: TransactionWithSigner,
        quantity: int,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        """Calls `sell_asset(pay,uint64)void` ABI method
        
        :param TransactionWithSigner buyer_txn: The `buyer_txn` ABI parameter
        :param int quantity: The `quantity` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[None]: The result of the transaction"""

        args = SellAssetArgs(
            buyer_txn=buyer_txn,
            quantity=quantity,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def get_asset_id(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[int]:
        """Calls `get_asset_id()uint64` ABI method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[int]: The result of the transaction"""

        args = GetAssetIdArgs()
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def create_bare(
        self,
        *,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Creates an application using the no_op bare method
        
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.TransactionResponse: The result of the transaction"""

        result = self.app_client.create(
            call_abi_method=False,
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
        )
        return result

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Calls the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass
        :returns algokit_utils.TransactionResponse: The result of the transaction"""
    
        return self.app_client.clear_state(_convert_transaction_parameters(transaction_parameters), app_args)

    def deploy(
        self,
        version: str | None = None,
        *,
        signer: TransactionSigner | None = None,
        sender: str | None = None,
        allow_update: bool | None = None,
        allow_delete: bool | None = None,
        on_update: algokit_utils.OnUpdate = algokit_utils.OnUpdate.Fail,
        on_schema_break: algokit_utils.OnSchemaBreak = algokit_utils.OnSchemaBreak.Fail,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        create_args: algokit_utils.DeployCallArgs | None = None,
        update_args: algokit_utils.DeployCallArgs | None = None,
        delete_args: algokit_utils.DeployCallArgs | None = None,
    ) -> algokit_utils.DeployResponse:
        """Deploy an application and update client to reference it.
        
        Idempotently deploy (create, update/delete if changed) an app against the given name via the given creator
        account, including deploy-time template placeholder substitutions.
        To understand the architecture decisions behind this functionality please see
        <https://github.com/algorandfoundation/algokit-cli/blob/main/docs/architecture-decisions/2023-01-12_smart-contract-deployment.md>
        
        ```{note}
        If there is a breaking state schema change to an existing app (and `on_schema_break` is set to
        'ReplaceApp' the existing app will be deleted and re-created.
        ```
        
        ```{note}
        If there is an update (different TEAL code) to an existing app (and `on_update` is set to 'ReplaceApp')
        the existing app will be deleted and re-created.
        ```
        
        :param str version: version to use when creating or updating app, if None version will be auto incremented
        :param algosdk.atomic_transaction_composer.TransactionSigner signer: signer to use when deploying app
        , if None uses self.signer
        :param str sender: sender address to use when deploying app, if None uses self.sender
        :param bool allow_delete: Used to set the `TMPL_DELETABLE` template variable to conditionally control if an app
        can be deleted
        :param bool allow_update: Used to set the `TMPL_UPDATABLE` template variable to conditionally control if an app
        can be updated
        :param OnUpdate on_update: Determines what action to take if an application update is required
        :param OnSchemaBreak on_schema_break: Determines what action to take if an application schema requirements
        has increased beyond the current allocation
        :param dict[str, int|str|bytes] template_values: Values to use for `TMPL_*` template variables, dictionary keys
        should *NOT* include the TMPL_ prefix
        :param algokit_utils.DeployCallArgs | None create_args: Arguments used when creating an application
        :param algokit_utils.DeployCallArgs | None update_args: Arguments used when updating an application
        :param algokit_utils.DeployCallArgs | None delete_args: Arguments used when deleting an application
        :return DeployResponse: details action taken and relevant transactions
        :raises DeploymentError: If the deployment failed"""

        return self.app_client.deploy(
            version,
            signer=signer,
            sender=sender,
            allow_update=allow_update,
            allow_delete=allow_delete,
            on_update=on_update,
            on_schema_break=on_schema_break,
            template_values=template_values,
            create_args=_convert_deploy_args(create_args),
            update_args=_convert_deploy_args(update_args),
            delete_args=_convert_deploy_args(delete_args),
        )

    def compose(self, atc: AtomicTransactionComposer | None = None) -> Composer:
        return Composer(self.app_client, atc or AtomicTransactionComposer())