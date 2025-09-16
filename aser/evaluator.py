import time
import json


class Evaluator:
    def __init__(self):
        self.results = []
    
    def evaluate_agent(self, agent,test_cases,check_function=None):

        if check_function == None:
            check_function = self._default_check


        evaluation_results = {
            "agent_name": agent.name,
            "total_tests": len(test_cases),
            "passed_tests": 0,
            "failed_tests": 0,
            "average_response_time": 0,
            "test_details": []
        }
        
        total_time = 0
        
        for i, test_case in enumerate(test_cases):
            start_time = time.time()
            
            try:
              
                response = agent.chat(test_case["input"])

                response_time = time.time() - start_time
                total_time += response_time
                
           
                is_correct = check_function(response, test_case["expected"])
                
                test_result = {
                    "test_id": i + 1,
                    "input": test_case["input"],
                    "expected": test_case["expected"],
                    "actual": response,
                    "response_time": response_time,
                    "passed": is_correct
                }
                
                if is_correct:
                    evaluation_results["passed_tests"] += 1
                else:
                    evaluation_results["failed_tests"] += 1
                
                evaluation_results["test_details"].append(test_result)
                
            except Exception as e:
                test_result = {
                    "test_id": i + 1,
                    "input": test_case["input"],
                    "expected": test_case["expected"],
                    "actual": f"Error: {str(e)}",
                    "response_time": 0,
                    "passed": False
                }
                evaluation_results["failed_tests"] += 1
                evaluation_results["test_details"].append(test_result)
        
  
        if len(test_cases) > 0:
            evaluation_results["average_response_time"] = total_time / len(test_cases)
        
   
        evaluation_results["accuracy"] = evaluation_results["passed_tests"] / evaluation_results["total_tests"]
        
        return evaluation_results
    
    def _default_check(self, actual: str, expected: str) -> bool:

  
        actual_lower = actual.lower()
        expected_lower = expected.lower()
        
      
        expected_keywords = expected_lower.split()
        matches = sum(1 for keyword in expected_keywords if keyword in actual_lower)
        
        
        return matches / len(expected_keywords) >= 0.5
    
    def print_summary(self, results):
        print(f"\n=== Evaluation Summary ===")
        print(f"Agent/Team: {results.get('agent_name', results.get('team_name', 'Unknown'))}")
        print(f"Total Tests: {results['total_tests']}")
        print(f"Passed: {results['passed_tests']}")
        print(f"Failed: {results['failed_tests']}")
        print(f"Accuracy: {results.get('accuracy', 0):.2%}")
        print(f"Average Response Time: {results.get('average_response_time', 0):.2f}s")