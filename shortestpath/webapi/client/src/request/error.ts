export enum KnownError {
    "NETWORK_ERROR" = "A network error happened while requesting data",
    "NOT_FOUND" = "Not Found",
    "INTERNAL_ERROR" = "Internal Error",
    "UNAUTHORIZED" = "Unauthorized",
    "CONFLICT" = "Conflict"
}

export const giveErrorFromStatusCode = (status: number) => {
    switch (status) {
        case 500: {
            return KnownError.INTERNAL_ERROR;
        }
        default: {
            return null;
        }
    }
};