import { ErrorType } from "@home/components/pages/home/ErrorDisplay";
import { ErrorResponse, KnownError, giveErrorFromStatusCode } from "./error";

export interface ArticleTitle {
    original_title: string;
    redirect_to_title: string;
}

export class FindShortestPathError extends Error {
    type: KnownError;
    additionalInfo: string;

    constructor(type: KnownError, additionalInfo: string) {
        super(type);
        this.type = type;
        this.additionalInfo = additionalInfo;
    }
}

export const FindShortestPath = async (from: string, to: string): Promise<ArticleTitle[]> => {
    const searchParams = new URLSearchParams({from, to})
    const response = await fetch(`${BUILDCONFIG.apiURL}/find_path?${searchParams}`, {
        method: "GET",
        redirect: "follow",
        
    }).catch(() => {
        throw new FindShortestPathError(KnownError.NETWORK_ERROR, "");
    });

    const errorVal = giveErrorFromStatusCode(response.status);

    if (errorVal != null) {
        if (errorVal === KnownError.INVALID_PARAMETER) {
            const responseJSON: ErrorResponse = await response.json();

            throw new FindShortestPathError(KnownError.INVALID_PARAMETER, responseJSON.invalid[0]);
        }

        throw new FindShortestPathError(errorVal, "");
    }

    const responseJSON: {path: ArticleTitle[]} = await response.json();


    return responseJSON.path;
}
