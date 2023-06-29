import * as React from "react";
import { SearchArticleTitle } from "@home/request";
import { Input, ListGroup, ListGroupItem } from "reactstrap";

interface IProps {
    onInputChange: (value: string) => void;
}

function SearchInput(props: IProps) {
    const defaultVal: string[] = [] // So typescript doesnt cast to any[] xd
    const [inputResults, setInputResults] = React.useState(defaultVal);
    const [inputPreviousResults, setInputPreviousResults] = React.useState(defaultVal);

    async function handleInput1Change(event: React.ChangeEvent<HTMLInputElement>) {
        props.onInputChange(event.currentTarget.value);

        if (event.currentTarget.value == "") {
            setInputResults([]);
            return;
        }

        const searchResult = await SearchArticleTitle(event.currentTarget.value);
        setInputResults(searchResult);
    }

    function inputBlurEvent() {
        setInputResults([]);
        setInputPreviousResults(inputResults);
    }

    function inputFocusEvent() {
        setInputResults(inputPreviousResults);
    }

    return <>
        <Input bsSize="lg" onChange={handleInput1Change} onBlur={inputBlurEvent} onFocus={inputFocusEvent} />
        <ListGroup>
            <div style={{position: "absolute"}}>
                {inputResults.map(s => <ListGroupItem key={s}>{s}</ListGroupItem>)}
            </div>
        </ListGroup>
    </>
}

export default SearchInput;