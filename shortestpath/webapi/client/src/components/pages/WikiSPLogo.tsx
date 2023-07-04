import * as React from "react";
import wikilogo from "@home/static/wikipedia-logo.svg";

function WikiSPLogo() {
    return <div style={{textAlign: "center", margin: "auto"}} className="wikisp-logo">
        <svg height="auto" width="100%" viewBox="0 0 840 250" style={{maxHeight: "250px"}}>
            <image xlinkHref={wikilogo} width="90" height="90" x="0" y="160"/>
            <line x1="90" y1="205" x2="250" y2="115" stroke="#2b2b2b" strokeWidth="7" strokeLinecap="round">
                <animate attributeName="x2" from="90" to="250" dur="150ms"/>
                <animate attributeName="y2" from="205" to="115" dur="150ms"/>
            </line>
            <image xlinkHref={wikilogo} width="90" height="90" x="250" y="70">
                <animate attributeName="opacity" values="0;1" dur="140ms" />
            </image>
            <line x1="340" y1="115" x2="500" y2="205" stroke="#2b2b2b" strokeWidth="7" strokeLinecap="round">
                <animate attributeName="x2" from="340" to="500" dur="300ms" />
                <animate attributeName="y2" from="115" to="205" dur="300ms" />
            </line>
            <image xlinkHref={wikilogo} width="90" height="90" x="500" y="160">
                <animate attributeName="opacity" values="0;1" dur="290ms" />
            </image>
            <line x1="590" y1="205" x2="750" y2="115" stroke="#2b2b2b" strokeWidth="7" strokeLinecap="round">
                <animate attributeName="x2" from="590" to="750" dur="450ms" />
                <animate attributeName="y2" from="205" to="115" dur="450ms" />
            </line>
            <image xlinkHref={wikilogo} width="90" height="90" x="750" y="70">
                <animate attributeName="opacity" values="0;1" dur="440ms" />
            </image>
        </svg>
        <h1 id="wikisp-title"><span className="wikisp-title-larger">W</span>IKIS<span className="wikisp-title-larger">P</span></h1>
    </div>
}

export default WikiSPLogo;