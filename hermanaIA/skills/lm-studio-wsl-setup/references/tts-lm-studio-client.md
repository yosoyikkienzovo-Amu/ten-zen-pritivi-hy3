# LM Studio TTS Client (Test-Time Compute)
# Source: Kamisama Kumi via Ikki, validated session 2026-05-05

class LMStudioClient:
    def __init__(self, base_url="http://localhost:1234/v1"):
        self.base_url = base_url
        self.chat_endpoint = f"{base_url}/chat/completions"
        self.models_endpoint = f"{base_url}/models"
    
    def chat(self, messages, model=None, temperature=0.7, 
             max_tokens=2000, stream=False):
        """
        messages: [{"role": "system/user/assistant", "content": "..."}]
        """
        payload = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        if model:
            payload["model"] = model
            
        try:
            response = requests.post(
                self.chat_endpoint,
                json=payload,
                timeout=120
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def think_deep(self, prompt, reasoning_steps=3):
        """
        Chain-of-Thought recursivo para razonamiento profundo
        """
        thoughts = []
        current_prompt = prompt
        
        for step in range(reasoning_steps):
            messages = [
                {"role": "system", "content": "Eres un pensador profundo. Analiza paso a paso."},
                {"role": "user", "content": f"Paso {step+1}/{reasoning_steps}: {current_prompt}"}
            ]
            
            response = self.chat(messages, temperature=0.3)
            thought = response['choices'][0]['message']['content']
            thoughts.append(thought)
            
            # El siguiente paso reflexiona sobre el anterior
            current_prompt = f"Reflexiona sobre esto: {thought}"
        
        return {
            "final_thought": thoughts[-1],
            "reasoning_chain": thoughts,
            "steps": reasoning_steps
        }
    
    def get_available_models(self):
        """Lista modelos cargados en LM Studio"""
        try:
            response = requests.get(self.models_endpoint)
            return response.json()
        except:
            return {"error": "LM Studio no responde"}

# EJEMPLO DE USO:
# client = LMStudioClient()
# result = client.think_deep(
#     prompt="¿Cómo puedo mejorar la seguridad de mi WSL?",
#     reasoning_steps=3
# )
# print(result["final_thought"])
