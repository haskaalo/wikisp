import { KnownError, giveErrorFromStatusCode } from "./error";

export interface ArticleTitle {
    original_title: string;
    redirect_to_title: string;
}

export const FindShortestPath = async (from: string, to: string): Promise<ArticleTitle[]> => {
    const searchParams = new URLSearchParams({from, to})
    const response = await fetch(`${BUILDCONFIG.apiURL}/find_path?${searchParams}`, {
        method: "GET",
        redirect: "follow",
        
    }).catch(() => {
        throw new Error(KnownError.NETWORK_ERROR);
    });

    const errorVal = giveErrorFromStatusCode(response.status);

    if (errorVal != null) {
        throw new Error(errorVal);
    }

    const responseJSON: {path: ArticleTitle[]} = await response.json();


    return responseJSON.path;
}
