import * as React from "react";
import { SearchArticleTitle, GetRandomArticleTitles } from "@home/request";
import { Input, ListGroup, ListGroupItem } from "reactstrap";

interface IProps {
    onInputChange: (value: string) => void;
    disabled: boolean
}

function SearchInput(props: IProps) {
    const defaultVal: string[] = [] // So typescript doesnt cast to any[] xd
    const [inputResults, setInputResults] = React.useState(defaultVal);
    const [inputPreviousResults, setInputPreviousResults] = React.useState(defaultVal);
    const [inputPlaceholderVal, setInputPlaceholderVal] = React.useState("");
    const [inputVal, setInputVal] = React.useState("");

    async function handleInputChange(event: React.ChangeEvent<HTMLInputElement>) {
        setInputVal(event.currentTarget.value);
        props.onInputChange(event.currentTarget.value);

        if (event.currentTarget.value == "") {
            setInputResults([]);
            return;
        }

        // TODO: catch error lol
        const searchResult = await SearchArticleTitle(event.currentTarget.value);
        setInputResults(searchResult);
    }

    function hideSearch() {
        setInputResults([]);
        setInputPreviousResults(inputResults);
    }

    function inputBlurEvent(e: React.FocusEvent) {
        // Search item has been pressed so we need to skip call to hideSearch
        // and allow onClick to be called
        if (e.relatedTarget != null && e.relatedTarget.classList.contains("search-item")) {
            return;
        }

        hideSearch();
    }

    function inputFocusEvent() {
        setInputResults(inputPreviousResults);
    }

    function handleSearchItemClick(query: string) {
        setInputVal(query);
        props.onInputChange(query);
        hideSearch();
    }

    React.useEffect(() => {
        const interval = setInterval(async () => {
            const articleTitles = await GetRandomArticleTitles();
            let newVal = articleTitles[Math.floor(Math.random() * articleTitles.length)];

            for (let i = 0; i < newVal.length; i++) {
                setInputPlaceholderVal(newVal.slice(0, i+1));
                await new Promise(r => setTimeout(r, Math.ceil(1000 / newVal.length)));
            }
            await new Promise(r => setTimeout(r, 1000));

            // If you ever wonder why i dont use inputPlaceholderVal, its cus its empty for some reason
            const initialLength = newVal.length;
            while (newVal.length > 0) {
                newVal = newVal.slice(0, newVal.length - 1)
                setInputPlaceholderVal(newVal.slice(0, newVal.length - 1));
                
                await new Promise(r => setTimeout(r, 1000 / initialLength));
            }
        }, 3500);

        return () => clearInterval(interval);
    }, []);

    if (props.disabled && inputResults.length > 0) {
        hideSearch();
    }
    
    return <>
        <Input bsSize="lg" onChange={handleInputChange} onBlur={inputBlurEvent} onFocus={inputFocusEvent}
        value={inputVal}
        placeholder={inputPlaceholderVal} 
        className="shadow"
        disabled={props.disabled}
        />
        <ListGroup hidden={props.disabled} style={{position: "absolute"}}>
            {inputResults.map(s => <ListGroupItem key={s} onClick={() => handleSearchItemClick(s)} className="search-item" tabIndex={0}>
                {s}</ListGroupItem>)}
        </ListGroup>
    </>
}

export default SearchInput;