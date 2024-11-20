#include <stdio.h>
#include <cstdlib>
#include <curl/curl.h>

int main()
{
    const char *openai_api_key = std::getenv("OPENAI_API_KEY");

    if (!openai_api_key)
    {
        printf("OPENAI_API_KEY is not set\n");
        return 1;
    }

    printf("%s", openai_api_key);

    return 0;
}