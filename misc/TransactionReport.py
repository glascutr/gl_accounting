# SELECT tr.date as 'Date', tr.particulars as 'Particulars', tr.cheque as 'Cheque', tr.voucher_type as 'Vouchar Type', tr.folio_no as 'Folio No.', tr.type as 'Type', tr.amount as 'Amount', ah.name1 as 'Account Head' FROM tabTransaction tr INNER JOIN tabAccounts Head ah ON tr.accounts_head = ah.name WHERE tr.date BETWEEN % (from_date)s AND % (to_date)s ORDER BY tr.modified DESC


SELECT 
    DATE_FORMAT(tr.date, '%%d-%%m-%%Y') AS 'Date',
    tr.particulars AS 'Particulars',
    tr.cheque AS 'Cheque',
    tr.voucher_type AS 'Voucher Type',
    tr.folio_no AS 'Folio No.',

    -- Type-wise columns
    CASE WHEN tr.type = 'Cash Amount' THEN tr.amount ELSE '' END AS 'Cash Amount',
    CASE WHEN tr.type = 'Expencess Amount' THEN tr.amount ELSE '' END AS 'Expencess Amount',
    CASE WHEN tr.type = 'Bank Debit' THEN tr.amount ELSE '' END AS 'Bank Debit',
    CASE WHEN tr.type = 'Bank Credit' THEN tr.amount ELSE '' END AS 'Bank Credit',
    
    ah.name1 AS 'Account Head'
    

FROM `tabTransaction` tr
INNER JOIN `tabAccounts Head` ah
    ON tr.accounts_head = ah.name
WHERE tr.date BETWEEN %(from_date)s AND %(to_date)s
ORDER BY tr.modified DESC;
