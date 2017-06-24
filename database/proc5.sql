SELECT description, statement
FROM navlinks
LEFT JOIN statements ON statements.parent = navlinks.id;