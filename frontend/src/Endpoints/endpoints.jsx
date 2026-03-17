const endpoints = {
  chat: {
    GENERAL: "/ai/policy_insurance_assistant/",
    RESET: "/users/reset_chat_history/",
    QUICK: "/ai/quick_search/",
    HISTORY: "/users/history/",
    STREAM: "/ai/experimental_streaming_assistant/",
  },

  auth: {
    LOGGIN: "/users/login/",
    SIGN_UP: "/users/register/",
  },
};

export default endpoints;
