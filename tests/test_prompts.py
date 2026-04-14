"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

PROMPT_V2_PATH = str(Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml")


def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


@pytest.fixture
def prompt_data():
    """Fixture que carrega os dados do prompt v2."""
    data = load_prompts(PROMPT_V2_PATH)
    return data["bug_to_user_story_v2"]


class TestPrompts:
    def test_prompt_has_system_prompt(self, prompt_data):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in prompt_data, "Campo 'system_prompt' não encontrado"
        assert prompt_data["system_prompt"] is not None, "system_prompt é None"
        assert len(prompt_data["system_prompt"].strip()) > 0, "system_prompt está vazio"

    def test_prompt_has_role_definition(self, prompt_data):
        """Verifica se o prompt define uma persona (ex: 'Você é um Product Manager')."""
        system_prompt = prompt_data["system_prompt"].lower()
        role_keywords = ["você é", "voce é", "você é um", "atue como", "seu papel"]
        has_role = any(keyword in system_prompt for keyword in role_keywords)
        assert has_role, "Prompt não define uma persona/role (ex: 'Você é um Product Manager')"

    def test_prompt_mentions_format(self, prompt_data):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = prompt_data["system_prompt"].lower()
        format_keywords = [
            "user story", "como um", "eu quero", "para que",
            "critérios de aceitação", "criterios de aceitacao",
            "dado que", "quando", "então", "entao",
            "markdown", "formato"
        ]
        matches = [kw for kw in format_keywords if kw in system_prompt]
        assert len(matches) >= 2, (
            f"Prompt não menciona formato adequado. "
            f"Esperado pelo menos 2 keywords de formato, encontrado: {matches}"
        )

    def test_prompt_has_few_shot_examples(self, prompt_data):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = prompt_data["system_prompt"]
        example_keywords = ["exemplo", "Exemplo", "EXEMPLO", "Entrada", "Saída", "entrada", "saída"]
        has_examples = any(keyword in system_prompt for keyword in example_keywords)
        assert has_examples, "Prompt não contém exemplos de Few-shot Learning (entrada/saída)"

        example_count = system_prompt.lower().count("exemplo")
        assert example_count >= 2, (
            f"Prompt deve ter pelo menos 2 exemplos de Few-shot, encontrado: {example_count}"
        )

    def test_prompt_no_todos(self, prompt_data):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        system_prompt = prompt_data.get("system_prompt", "")
        user_prompt = prompt_data.get("user_prompt", "")
        full_text = system_prompt + " " + user_prompt

        assert "[TODO]" not in full_text, "Prompt contém [TODO] não resolvido"
        assert "TODO:" not in full_text, "Prompt contém TODO: não resolvido"
        assert "FIXME" not in full_text, "Prompt contém FIXME não resolvido"

    def test_minimum_techniques(self, prompt_data):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        assert "techniques_applied" in prompt_data, (
            "Campo 'techniques_applied' não encontrado nos metadados"
        )
        techniques = prompt_data["techniques_applied"]
        assert isinstance(techniques, list), "techniques_applied deve ser uma lista"
        assert len(techniques) >= 2, (
            f"Mínimo de 2 técnicas requeridas, encontradas: {len(techniques)} - {techniques}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
