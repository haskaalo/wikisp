import * as React from "react";
import { ArticleTitle } from "@home/request";
import { Container, Col } from "reactstrap";

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

        const nextArrow = <>&rarr;</>;

        return <>
        <Col key={title} md>
            {title} {lastElem ? null : nextArrow}
        </Col>
        </>;
    }

    return <>
        {indexedPath.map(article => pathBuilder(article.idx, article.val))}
    </>
}

export default PathDisplay;
