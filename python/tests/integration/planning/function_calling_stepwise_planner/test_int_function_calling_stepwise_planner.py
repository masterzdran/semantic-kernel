# Copyright (c) Microsoft. All rights reserved.

import pytest

from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion,
)
from semantic_kernel.core_plugins.math_plugin import MathPlugin
from semantic_kernel.kernel import Kernel
from semantic_kernel.planners.function_calling_stepwise_planner.function_calling_stepwise_planner import (
    FunctionCallingStepwisePlanner,
)
from semantic_kernel.planners.function_calling_stepwise_planner.function_calling_stepwise_planner_options import (
    FunctionCallingStepwisePlannerOptions,
)
from semantic_kernel.planners.function_calling_stepwise_planner.function_calling_stepwise_planner_result import (
    FunctionCallingStepwisePlannerResult,
)


@pytest.mark.asyncio
async def test_can_execute_function_calling_stepwise_plan(kernel: Kernel, get_oai_config):
    api_key, _ = get_oai_config

    service_id = "planner"
    kernel.add_service(
        OpenAIChatCompletion(
            service_id=service_id,
            ai_model_id="gpt-3.5-turbo-1106",
            api_key=api_key,
        ),
    )

    kernel.add_plugin(MathPlugin(), "MathPlugin")

    questions = [
        "What is the current hour number, plus 5?",
    ]

    options = FunctionCallingStepwisePlannerOptions(
        max_iterations=5,
        max_tokens=1000,
    )

    planner = FunctionCallingStepwisePlanner(service_id=service_id, options=options)

    for question in questions:
        result = await planner.invoke(kernel, question)
        print(f"Q: {question}\nA: {result.final_answer}\n")
        assert isinstance(result, FunctionCallingStepwisePlannerResult)
        assert 0 < len(result.final_answer) < 100
