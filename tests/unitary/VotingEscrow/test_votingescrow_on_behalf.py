import brownie


# deposit_for_on_behalf
# -reverts if msg.sender does not have enough balance
# -revert if sending no tokens
# -revert if no existing lock
# -revert if lock already ended
# -check ERC20 transfer is successful
# -check if locked amount numbers are correct of the sender and the victim
# -check after x time, the locked balance is approximately correct

# create_lock_on_behalf
# -if not admin then revert
# -if value is 0 revert
# -if user already has a lock then revert
# -if unlock_time is less than current timestamp then revert
# -if unlock_time is greater than maximum time then revert
# -check ERC20 transfer is successful
# -check if locked amount numbers are correct of the sender and the victim
# -check after x time, the locked balance is approximately correct

# batch_send
# -able to lock for 2 users
# -able to lock for 2 users and deposit for 2 users
# -able to lock for 100 users
# -able to deposit for 100 users
# -able to lock for 50 users and deposit for 50 users
