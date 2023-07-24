import { KnownError, giveErrorFromStatusCode } from "./error";

export const SearchArticleTitle = async (query: string): Promise<string[]> => {
    const searchParams = new URLSearchParams({q: query})
    const response = await fetch(`${BUILDCONFIG.apiURL}/search?${searchParams}`, {
        method: "GET",
        redirect: "follow",
        
    }).catch(() => {
        throw new Error(KnownError.NETWORK_ERROR);
    });

    const errorVal = giveErrorFromStatusCode(response.status);

    if (errorVal != null) {
        throw new Error(errorVal);
    }

    const responseJSON: {result: string[]} = await response.json();


    return responseJSON.result;
}