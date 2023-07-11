export enum KnownError {
    "NETWORK_ERROR" = "A network error happened while requesting data",
    "NOT_FOUND" = "Not Found",
    "INTERNAL_ERROR" = "Internal Error",
    "UNAUTHORIZED" = "Unauthorized",
    "CONFLICT" = "Conflict",
    "INVALID_PARAMETER" = "Invalid Parameter"
}

export const giveErrorFromStatusCode = (status: number) => {
    switch (status) {
        case 500: {
            return KnownError.INTERNAL_ERROR;
        }
        case 400: {
            return KnownError.INVALID_PARAMETER
        }
        default: {
            return null;
        }
    }
};

export interface ErrorResponse {
    status: number;
    message: string;
    invalid?: string[];
}