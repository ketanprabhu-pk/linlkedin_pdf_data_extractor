# linlkedin pdf data extractor
`linlkedin_pdf_data_extractor` gets the data extracted by the pdfstructure and sorts it accordingly to its respectrd dto according to the text size and traverse through document

`linlkedin_pdf_data_extractor` is built on top of [pdfstructure](https://github.com/ChrizH/pdfstructure). 

- Paragraph extraction is performed leveraging `pdfminer.high_level.extract_pages()`.
- Those paragraphs are then grouped together according to some basic (extendable) heuristics.

### read pdf document and 

Of course, encoded documents can be easily decoded and used for further analysis. 
However, detailed information like bounding boxes or coordinates for each character are not persisted.

```
    source = FileSource("./examples/profile.pdf")

    document = parser.parse_pdf(source)
    
    print(document.title)
```

## Traverse through document structure
Having all paragraphs and sections organised as a general tree, 
its straight forward to iterate through the layers and search for specific elements like headlines, or extract all main headers like chapter titles.  

Two document traversal generators are available that yield each section `in-order` or in `level-order` respectively. 
```
    from pdfstructure.hierarchy.traversal import traverse_in_order

    elements_flat_in_order = [element for element in traverse_in_order(document)]

    Exemplary illustration of yield order:
        """
                         5   10
                      /   \    \
                     1     2    3
                   / | \        |
                  a  b  c       x
    
        yield order:
        - [5,1,a,b,c,2,10,3,x]
        """
```

### to start 
```
sudo python3 setup.py install

pip3 install requirements.txt

python3 extractr.py

```