from database import get_db_connection


def get_account(username):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    connection.close()

    return dict(user) if user else None


def get_balance(username):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT name, balance, currency FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    connection.close()

    return dict(user) if user else None


def create_transfer(from_user, to_user, amount):

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        connection.execute("BEGIN")

        # Find the sender
        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (from_user,)
        )
        sender = cursor.fetchone()

        if sender is None:
            connection.rollback()
            return None, "Sender not found", 404

        # Find the recipient
        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (to_user,)
        )
        recipient = cursor.fetchone()

        if recipient is None:
            connection.rollback()
            return None, "Recipient not found", 404

        # Check sufficient funds
        if sender["balance"] < amount:
            connection.rollback()
            return None, "Insufficient funds", 400

        # Calculate new balances
        sender_balance = sender["balance"] - amount
        recipient_balance = recipient["balance"] + amount

        # Update sender
        cursor.execute(
            """
            UPDATE users
            SET balance = ?
            WHERE username = ?
            """,
            (sender_balance, from_user)
        )

        # Update recipient
        cursor.execute(
            """
            UPDATE users
            SET balance = ?
            WHERE username = ?
            """,
            (recipient_balance, to_user)
        )

        # Create temporary transaction ID
        cursor.execute(
            """
            INSERT INTO transactions
            (transaction_id, from_user, to_user, amount, currency, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "TEMP",
                from_user,
                to_user,
                amount,
                "USD",
                "completed"
            )
        )

        # Get the database-generated ID
        database_id = cursor.lastrowid

        # Create the final transaction ID
        transaction_id = f"TX{database_id:03d}"

        # Update the transaction ID
        cursor.execute(
            """
            UPDATE transactions
            SET transaction_id = ?
            WHERE id = ?
            """,
            (transaction_id, database_id)
        )

        connection.commit()

        transaction = {
            "transactionId": transaction_id,
            "status": "completed",
            "from": from_user,
            "to": to_user,
            "amount": amount,
            "currency": "USD"
        }

        return transaction, None, 201

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()