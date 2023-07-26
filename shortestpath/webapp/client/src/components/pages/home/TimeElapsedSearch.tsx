import * as React from "react";


function msTos(ms: number) {
    return Math.floor(ms / 1000);
}

function msToM(ms: number) {
    return Math.floor(ms / 60000);
}

function TimeElapsedSearch() {
    const beginning = performance.now();
    let [currentTime, setCurrentTime] = React.useState(0);

    function timeDisplay(interval: number) {
        const inMinutes = msToM(interval);
        const inSeconds = msTos(interval)

        let result = "";

        if (inMinutes > 0) result = `${inMinutes}m.${msTos(interval - (1000 * inSeconds))}s`
        else {
            let secondsDecimals = String(Math.floor((interval - (inSeconds * 1000))));
            
            while (secondsDecimals.length < 3) {
                secondsDecimals = "0" + secondsDecimals;
            }

            result = `${inSeconds}.${secondsDecimals}s`
        }

        return result;
    }

    React.useEffect(() => {
        const timeRenderInterval = setInterval(() => {
            setCurrentTime(performance.now() - beginning);
        }, 10);

        return () => clearInterval(timeRenderInterval);
    }, []);

    return <> ({timeDisplay(currentTime)})</>;
}

export default TimeElapsedSearch;