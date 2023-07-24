import { KnownError, giveErrorFromStatusCode } from "./error";

let randomArticleTitles: string[] = [];
let called = false;

export const GetRandomArticleTitles = async() => {
    // Prevent double call from the 2 inputs
    if (randomArticleTitles.length > 0) {
        return randomArticleTitles;
    } else if (called) {
        while (randomArticleTitles.length === 0) {
            await new Promise(r => setTimeout(r, 100));
        }

        return randomArticleTitles;
    }

    called = true;

    const response = await fetch(`${BUILDCONFIG.apiURL}/random_article_titles`, {
        method: "GET",
        redirect: "follow",
        
    }).catch(() => {
        called = false;
        throw new Error(KnownError.NETWORK_ERROR);
    });

    const errorVal = giveErrorFromStatusCode(response.status);

    if (errorVal != null) {
        called = false;
        throw new Error(errorVal);
    }

    randomArticleTitles = await response.json();
    return randomArticleTitles;
}