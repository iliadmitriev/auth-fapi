from passlib.context import CryptContext

# ctx.hash(secret)
# ctx.verify(secret, hash)
# ctx.needs_update(hash)
# ctx.verify_and_update(secret, hash)

password_hash_ctx = CryptContext(
    schemes=["pbkdf2_sha256"],
    pbkdf2_sha256__min_rounds=18000,
    pbkdf2_sha256__max_rounds=26000
)
