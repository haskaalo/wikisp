declare const BUILDCONFIG: {
    apiURL: string;
    captchaSiteKey: string;
    captchaEnabled: boolean;
}

declare module '*.svg';
declare module '*.jpg';

// Cloudflare turnstile
declare namespace turnstile {
    interface TurnstileSettingsInterface {
        sitekey: string;
        callback: (successToken: string) => void;
    }
    function render(element: string, callback: TurnstileSettingsInterface): void;
}
