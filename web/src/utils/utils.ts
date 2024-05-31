interface Params {
    [key: string]: string | number | boolean;
};

export function generateUrl(baseUrl: string, params: Params): string {
    const queryString = Object.entries(params)
        .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`)
        .join('&');
    return `${baseUrl}?${queryString}`;
};
