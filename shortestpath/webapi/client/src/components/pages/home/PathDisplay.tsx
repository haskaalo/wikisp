import * as React from "react";
import { ArticleTitle } from "@home/request";
import { Col } from "reactstrap";
import "./pathdisplay_style.scss";

interface IProps {
    path: ArticleTitle[];
}

function PathDisplay(props: IProps) {
    const indexedPath: {idx: number, val: ArticleTitle}[] = [];
    for (let i = 0; i < props.path.length; i++) {
        indexedPath.push({idx: i, val: props.path[i]});
    }

    function pathBuilder(idx: number, article: ArticleTitle) {
        const title = article.redirect_to_title === "" ? article.original_title : article.redirect_to_title;
        const lastElem = idx === indexedPath.length - 1;

        // For smaller screens

        const nextArrow = <Col md className="col-path">
            <div className="path-arrow">
                <svg width="30%" height="30%" viewBox="0 0 100 100">
                    <line x1="0" y1="50" x2="100" y2="50" stroke="black" strokeWidth="7" />
                    <line x1="45" y1="10" x2="100" y2="50" stroke="black" strokeWidth="7" />
                    <line x1="45" y1="90" x2="100" y2="50" stroke="black" strokeWidth="7" />
                </svg>
            </div>
        </Col>;

        return <React.Fragment key={title}>
          <Col md className="col-path">
            <div className="article-info">
                {title}
            </div>
        </Col>
        {lastElem ? null : nextArrow}
        </React.Fragment>;
    }

    return <>
        {indexedPath.map(article => pathBuilder(article.idx, article.val))}
    </>
}

export default PathDisplay;
