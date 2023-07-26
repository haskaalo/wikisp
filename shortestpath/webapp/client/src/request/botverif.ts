import { KnownError, giveErrorFromStatusCode } from "./error";

export function getStoredToken() {
    return localStorage.getItem("sess-token");
}

export function storeToken(token: string) {
    return localStorage.setItem("sess-token", token);
}

export function deleteToken() {
    localStorage.removeItem("sess-token");
}

interface getBotVerifResponse {
    success: boolean;
    token: string;
}

export async function doBotVerif(gRecaptchaResponse: string) {
    const response = await fetch(`${BUILDCONFIG.apiURL}/bot-verif?captchaResponse=${encodeURI(gRecaptchaResponse)}`, {
        method: "GET",
        redirect: "follow"
    }).catch((err) => {
        throw new Error(KnownError.NETWORK_ERROR);
    });

    const errorVal = giveErrorFromStatusCode(response.status);
    if (errorVal != null) {
        throw new Error(errorVal);
    }

    const responseJSON: getBotVerifResponse = await response.json();

    if (responseJSON.success) {
        storeToken(responseJSON.token);
        return true;
    } else {
        return false;
    }
}
